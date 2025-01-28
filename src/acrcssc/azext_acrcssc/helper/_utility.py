# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import re
from knack.log import get_logger
from datetime import (datetime, timezone)
import shutil
from azure.cli.core.azclierror import InvalidArgumentValueError
from ._constants import ERROR_MESSAGE_INVALID_TIMESPAN_VALUE, TMP_DRY_RUN_FILE_NAME
from azure.mgmt.core.tools import parse_resource_id
from ._constants import (
    ERROR_MESSAGE_INVALID_TIMESPAN_FORMAT,
    RESOURCE_GROUP,
    SCHEDULE_MIN_DAYS,
    SCHEDULE_MAX_DAYS
)
from .._client_factory import cf_acr_tasks

logger = get_logger(__name__)
# pylint: disable=logging-fstring-interpolation


# this is a cheaper regex to match than the cron expression
# Regex to look for pattern 1d, 2d, 3d, etc
def schedule_timespan_format(schedule):
    match = re.match(r'(\d+)d$', schedule)
    if match is not None:
        return int(match.group(1))
    return None


def convert_timespan_to_cron(schedule, date_time=None):
    # only timespan and cron formats are supported, and 'schedule' has already been validated
    match = schedule_timespan_format(schedule)
    if not match:
        return schedule

    if date_time is None:
        date_time = datetime.now(timezone.utc)

    cron_hour = date_time.hour
    cron_minute = date_time.minute

    if match < SCHEDULE_MIN_DAYS or match > SCHEDULE_MAX_DAYS:
        raise InvalidArgumentValueError(error_msg=ERROR_MESSAGE_INVALID_TIMESPAN_VALUE)
    cron_expression = f'{cron_minute} {cron_hour} */{match} * *'

    return cron_expression


def transform_cron_to_schedule(cron_expression, just_days=False):
    parts = cron_expression.split()
    # The third part of the cron expression
    third_part = parts[2]

    match = re.search(r'\*/(\d+)', third_part)

    if match:
        days = int(match.group(1))

        # cron expressions like "0 0 */99 * *" are valid (it will only trigger on the 1st of every month), but displaying it as days makes no sense.
        # Display the full cron expression so the user can see what's going on.
        if days < 1 or days > 31:
            return cron_expression

        if just_days:
            return days
        return f"{days}d"

    # if the cron expression is not in the format */n, return the cron expression as is
    return cron_expression


def create_temporary_dry_run_file(file_location, tmp_folder):
    templates_path = os.path.dirname(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            "../templates/"))
    logger.debug(f"templates_path:  {templates_path}")

    os.makedirs(tmp_folder, exist_ok=True)
    file_template_copy = templates_path + "/" + TMP_DRY_RUN_FILE_NAME

    shutil.copy2(file_template_copy, tmp_folder)
    shutil.copy2(file_location, tmp_folder)
    folder_contents = os.listdir(tmp_folder)
    logger.debug(f"Copied dry run file {folder_contents}")


def delete_temporary_dry_run_file(tmp_folder):
    logger.debug(f"Deleting contents and directory {tmp_folder}")
    shutil.rmtree(tmp_folder)


def get_task(cmd, registry, task_name, task_client=None):
    if task_client is None:
        task_client = cf_acr_tasks(cmd.cli_ctx)

    resourceid = parse_resource_id(registry.id)
    resource_group = resourceid[RESOURCE_GROUP]

    try:
        return task_client.get(resource_group, registry.name, task_name)
    except Exception as exception:
        logger.debug("Failed to find task %s from registry %s : %s", task_name, registry.name, exception)
        return None
