import logging
import json
from datetime import datetime, timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from requests import (Request, Session)

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util import Throttle
from homeassistant.const import (CONF_NAME)
CONF_STATION_ID = 'station_id'

DEFAULT_NAME = 'Cracow Air Quality'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Required(CONF_STATION_ID): cv.string,
  vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

class AirQualityData(object):
  def __init__(self, stationId):
    self.stationId = stationId
    self.table = {}
    self.update = Throttle(timedelta(minutes=30))(self._update)

  def _update(self):
    data_request = Request(
      "POST", 
      "http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz", 
      data=self._body()
    ).prepare()

    self.table = {}
    with Session() as sess:
      response = sess.send(data_request, timeout=10)
      data = json.loads(response.text)['data']
      for metric in data['series']:
        self.table[metric['paramId']] = metric

  def get(self, key):
    return self.table.get(key)

  def _body(self):
    return {
      'query': json.dumps({
        'measType': 'Auto',
        'viewType': 'Station',
        'viewTypeEntityId': self.stationId,
        'channels': [49,54,61,57,211,53,50,55],
        'dateRange': 'Day',
        'date': datetime.now().strftime("%d.%m.%Y")
      })
    }

class AirCracowQualitySensor(Entity):
  def __init__(self, data, metric_type, name):
    self.metric_type = metric_type
    self.data = data
    self._friendly_name = self.get('paramLabel')
    self._name = "{}_{}".format(name,metric_type)

  @property
  def friendly_name(self):
    return self._friendly_name

  @property
  def name(self):
    return self._name

  @property
  def state(self):
    return self.get('data')[-1][1]

  @property
  def unit_of_measurement(self):
    return self.get('unit')

  @property
  def icon(self):
    return "mdi:skull"

  def get(self, key):
    return self.data.get(self.metric_type).get(key)

  def update(self):
    self.data.update()

def setup_platform(hass, config, add_devices, discovery_info=None):
  stationId = config.get(CONF_STATION_ID)
  name = config.get(CONF_NAME)
  data = AirQualityData(stationId)
  data.update()

  sensors = []
  for metric_type in data.table:
    _LOGGER.info("Adding sensor: {}".format(metric_type))
    sensors.append(AirCracowQualitySensor(data, metric_type, name))
  add_devices(sensors, True)
