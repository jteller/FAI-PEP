#!/usr/bin/env python

##############################################################################
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
##############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json

from utils.utilities import requestsJson

NETWORK_TIMEOUT = 150


class DBDriver(object):
    def __init__(self, table, job_queue, is_test, db_entry):
        self.table = table
        self.job_queue = job_queue

        assert db_entry != "", "Database entry cannot be empty"

        self.db_entry = db_entry

    def submitBenchmarks(self, data, devices, identifier, user):
        json_data = json.dumps(data)
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'add',
            'identifier': identifier,
            'devices': devices,
            'benchmarks': json_data,
            'user': user,
        }
        self._requestData(params)

    def claimBenchmarks(self, server_id, devices):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'claim',
            'claimer': server_id,
            'devices': devices,
        }
        result_json = self._requestData(params)
        return self._processBenchmarkResults(result_json['values'])

    def releaseBenchmarks(self, server_id, ids):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'release',
            'claimer': server_id,
            'ids': ids,
        }
        self._requestData(params)

    def runBenchmarks(self, server_id, ids):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'run',
            'claimer': server_id,
            'ids': ids,
        }
        self._requestData(params)

    def doneBenchmarks(self, id, status, result, log):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'done',
            'id': id,
            'status': status,
            'result': result,
            'log': log,
        }
        self._requestData(params)

    def statusBenchmarks(self, identifier):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'status',
            'identifier': identifier,
        }
        request_json = self._requestData(params)
        return request_json["values"]

    def getBenchmarks(self, ids):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'get',
            'ids': ids,
        }
        request_json = self._requestData(params)
        return request_json["values"]

    def updateDevices(self, server_id, devices, reset):
        params = {
            'table': self.table,
            'job_queue': self.job_queue,
            'action': 'update_devices',
            'claimer': server_id,
            'devices': devices,
        }
        if reset:
            params["reset"] = "true"
        self._requestData(params)

    def listDevices(self, job_queue):
        params = {
            'table': self.table,
            'job_queue': job_queue,
            'action': 'list_devices',
        }
        result_json = self._requestData(params)
        return result_json["values"]

    def _requestData(self, params):
        result_json = requestsJson(self.db_entry,
                                   data=params, timeout=NETWORK_TIMEOUT)
        if "status" not in result_json or result_json['status'] != "success":
            return {
                "status": "fail",
                "values": [],
            }
        else:
            return result_json

    def _processBenchmarkResults(self, result_json):
        for result in result_json:
            benchmarks = json.loads(result["benchmarks"])
            result["benchmarks"] = benchmarks
        return result_json
