# Testing of WP-Cron

## WP-CLI

Cron jobs can be tested usingWP-CLI. It offers commands like```wp cron event list```and```wp cron event run {job name}```.Check the documentationfor more details.

## WP-Cron Management Plugins

Several plugins are available on the WordPress.org Plugin Directory for viewing, editing, and controlling the scheduled cron events and available schedules on your site.

## _get_cron_array()

The```_get_cron_array()```functionreturns an array of all currently scheduled cron events. Use this function if you need to inspect the raw list of events.

## wp_get_schedules()

The```wp_get_schedules()```functionreturns an array of available event recurrence schedules. Use this function if you need to inspect the raw list of available schedules.
