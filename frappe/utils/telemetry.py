""" Basic telemetry for improving apps.

WARNING: Everything in this file should be treated "internal" and is subjected to change or get
removed without any warning.
"""
from contextlib import suppress

from posthog import Posthog

import frappe

POSTHOG_PROJECT_FIELD = "posthog_project_id"
POSTHOG_HOST_FIELD = "posthog_host"


def add_bootinfo(bootinfo):
	if not frappe.get_system_settings("enable_telemetry"):
		return

	bootinfo.posthog_host = frappe.conf.get(POSTHOG_HOST_FIELD)
	bootinfo.posthog_project_id = frappe.conf.get(POSTHOG_PROJECT_FIELD)
	bootinfo.enable_telemetry = True


def init_telemetry():
	"""Init posthog for server side telemetry."""
	if hasattr(frappe.local, "posthog"):
		return

	if not frappe.get_system_settings("enable_telemetry"):
		return

	posthog_host = frappe.conf.get(POSTHOG_HOST_FIELD)
	posthog_project_id = frappe.conf.get(POSTHOG_PROJECT_FIELD)

	if not posthog_host or not posthog_project_id:
		return

	with suppress(Exception):
		frappe.local.posthog = Posthog(posthog_project_id, host=posthog_host)


def capture(event, app):
	init_telemetry()
	ph: Posthog = getattr(frappe.local, "posthog", None)
	with suppress(Exception):
		ph and ph.capture(frappe.local.site, f"{app}_{event}")
