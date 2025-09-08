from .const import DOMAIN

from homeassistant import config_entries


class ExposeCameraStreamSourceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return self.async_create_entry(title="Expose Camera Stream Source", data={})
