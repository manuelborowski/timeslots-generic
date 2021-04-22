from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm
from app import db, log, admin_required, data
from app.application import socketio as msocketio, event as mevent, guest as mguest
from . import settings
from app.application import settings as msettings
from app.presentation.layout.utils import flash_plus, button_pressed

@settings.route('/settings', methods=['GET', 'POST'])
@admin_required
@login_required
def show():
    default_settings = msettings.get_configuration_settings()
    return render_template('/settings/settings.html',
                           settings_form=settings_formio, default_settings=default_settings)


@settings.route('/settings/upload_guest_info', methods=['GET', 'POST'])
@admin_required
@login_required
def upload_guest_info():
    try:
        if request.files['guest_info_file']:
            mguest.import_guest_info(request.files['guest_info_file'])
        flash_plus('Guest info file is imported')
        return redirect(url_for('settings.show'))
    except Exception as e:
        flash_plus('Could not import guest file', e)



def update_settings_cb(msg, client_sid=None):
    msettings.set_configuration_setting(msg['data']['setting'], msg['data']['value'])


def event_received_cb(msg, client_sid=None):
    mevent.process_event(msg['data']['event'])

msocketio.subscribe_on_type('settings', update_settings_cb)
msocketio.subscribe_on_type('event', event_received_cb)


from app.presentation.view import false, true, null

# https://formio.github.io/formio.js/app/builder
settings_formio = \
    {
  "display": "form",
  "components": [
    {
      "title": "Algemeen",
      "theme": "primary",
      "collapsible": true,
      "key": "algemeen",
      "type": "panel",
      "label": "Algemeen",
      "input": false,
      "tableView": false,
      "components": [
        {
          "label": "Uitnodigingse-mails worden verzonden",
          "tableView": false,
          "defaultValue": false,
          "persistent": false,
          "key": "enable-send-invite-email",
          "type": "checkbox",
          "input": true
        },
        {
          "label": "Bevestigingse-mails worden verzonden",
          "tableView": false,
          "defaultValue": false,
          "persistent": false,
          "key": "enable-send-ack-email",
          "type": "checkbox",
          "input": true
        },
        {
          "label": "Columns",
          "columns": [
            {
              "components": [
                {
                  "label": "Opgepast: stuur een uitnodiging naar alle gasten",
                  "tableView": false,
                  "key": "checkbox-enable-send-invite",
                  "type": "checkbox",
                  "input": true,
                  "defaultValue": false,
                  "hideOnChildrenHidden": false
                }
              ],
              "width": 6,
              "offset": 0,
              "push": 0,
              "pull": 0,
              "size": "md"
            },
            {
              "components": [
                {
                  "label": "Stuur uitnodigingse-mails naar alle gasten",
                  "action": "event",
                  "showValidations": false,
                  "theme": "danger",
                  "tableView": false,
                  "key": "button-send-invite-emails",
                  "conditional": {
                    "show": true,
                    "when": "checkbox-enable-send-invite",
                    "eq": "true"
                  },
                  "type": "button",
                  "input": true,
                  "event": "button-send-invite-emails",
                  "hideOnChildrenHidden": false
                }
              ],
              "width": 6,
              "offset": 0,
              "push": 0,
              "pull": 0,
              "size": "md"
            }
          ],
          "key": "columns",
          "type": "columns",
          "input": false,
          "tableView": false
        }
      ],
      "collapsed": true
    },
    {
      "title": "BEZOEKERS : Registratie template en e-mail",
      "theme": "primary",
      "collapsible": true,
      "key": "RegistratieTemplate1",
      "type": "panel",
      "label": "BEZOEKERS : Registratie template en e-mail",
      "input": false,
      "tableView": false,
      "components": [
        {
          "label": "Uitnodigings email: onderwerp",
          "autoExpand": false,
          "tableView": true,
          "key": "invite-mail-subject-template",
          "type": "textarea",
          "input": true
        },
        {
          "label": "Uitnodigings email: inhoud",
          "autoExpand": false,
          "tableView": true,
          "key": "invite-mail-content-template",
          "type": "textarea",
          "input": true
        },
        {
          "label": "Web registratie template",
          "autoExpand": false,
          "tableView": true,
          "key": "register-template",
          "type": "textarea",
          "input": true
        },
        {
          "label": "Registratie bevestigingse-mail: onderwerp",
          "autoExpand": false,
          "tableView": true,
          "persistent": false,
          "key": "register-mail-ack-subject-template",
          "type": "textarea",
          "input": true
        },
        {
          "label": "Registratie bevestigingse-mail: inhoud",
          "autoExpand": false,
          "tableView": true,
          "persistent": false,
          "key": "register-mail-ack-content-template",
          "type": "textarea",
          "input": true
        }
      ],
      "collapsed": true
    },
    {
      "title": "E-mail server settings",
      "theme": "primary",
      "collapsible": true,
      "key": "eMailServerSettings",
      "type": "panel",
      "label": "E-mail server settings",
      "input": false,
      "tableView": false,
      "components": [
        {
          "label": "Aantal keer dat een e-mail geprobeerd wordt te verzenden",
          "labelPosition": "left-left",
          "mask": false,
          "spellcheck": false,
          "tableView": false,
          "delimiter": false,
          "requireDecimal": false,
          "inputFormat": "plain",
          "key": "email-send-max-retries",
          "type": "number",
          "input": true
        },
        {
          "label": "Tijd (seconden) tussen het verzenden van e-mails",
          "labelPosition": "left-left",
          "mask": false,
          "spellcheck": true,
          "tableView": false,
          "persistent": false,
          "delimiter": false,
          "requireDecimal": false,
          "inputFormat": "plain",
          "key": "email-task-interval",
          "type": "number",
          "input": true
        },
        {
          "label": "Max aantal e-mails per minuut",
          "labelPosition": "left-left",
          "mask": false,
          "spellcheck": true,
          "tableView": false,
          "persistent": false,
          "delimiter": false,
          "requireDecimal": false,
          "inputFormat": "plain",
          "key": "emails-per-minute",
          "type": "number",
          "input": true
        },
        {
          "label": "Basis URL",
          "labelPosition": "left-left",
          "tableView": true,
          "key": "base-url",
          "type": "textfield",
          "input": true
        },
        {
          "label": "E-mails mogen worden verzonden",
          "tableView": false,
          "persistent": false,
          "key": "enable-send-email",
          "type": "checkbox",
          "input": true,
          "defaultValue": false
        }
      ],
      "collapsed": true
    }
  ]
}

