import os
import nose.tools             as nose
import helper.application     as app_helper
import helper.db              as db_helper
import nucleotides.api_client as api

def test_fetch_task_from_valid_url():
    db_helper.reset_database()
    response = api.fetch_task("1", app_helper.mock_short_read_assembler_state(task = False))
    nose.assert_in("id", response)
    nose.assert_equal(response["id"], 1)

@nose.raises(IOError)
def test_fetch_task_from_invalid_url():
    app = app_helper.mock_short_read_assembler_state(task = False)
    app["api"] = "localhost:98765"
    response = api.fetch_task("1", app)

def test_post_event():
    db_helper.reset_database()
    event = {"task" : 1,
             "success" : False,
             "files" : [
                 {"url"    : "s3://url",
                  "sha256" : "adef5c",
                  "type"   : "log" } ] }
    api.post_event(event, app_helper.mock_short_read_assembler_state(task = False))
