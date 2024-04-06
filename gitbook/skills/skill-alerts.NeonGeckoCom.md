---
description: short description
---

### _skill-alerts.NeonGeckoCom_  
## Description:  
The skill provides functionality to create alarms, timers and reminders, remove them by name, time, or type, and ask for
what is active. You may also silence all alerts and ask for a summary of what was missed if you were away, your device
was off, or you had quiet hours enabled.

Alarms and reminders may be set to recur daily or weekly. An active alert may be snoozed for a specified amount of time
while it is active. Any alerts that are not acknowledged will be added to a list of missed alerts that may be read and
cleared when requested.

Other modules may integrate with the alerts skill by listening for `neon.alert_expired` events. This event will be
emitted when a scheduled alert expires and will include any context associated with the event creation. If the event
was created with `mq` context, the mq connector module will forward the expired alert for the client module to handle
and the alert will be marked `active` until the client module emits a `neon.acknowledge_alert` Message with the `alert_id`
and `missed` data, i.e.:
```
Message("neon.acknowledge_alert", {"alert_id": , "missed": False}, )
```  
  
  
  
## Summary:  
