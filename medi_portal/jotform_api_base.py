from libs.jotform.jotform import *

class JotformAPIBase():
    def __init__(self, api_key, arg):
        super(JotformAPIBase, self).__init__()
        self.api_key = api_key
        self.base_url = arg['base_url']              
        self.team_id = arg['team_id']
        self.jotform_api_conn = self.connect_api()

    def connect_api(self):
        jotformAPIClient = JotformAPIClient(self.api_key)
        return jotformAPIClient

    def get_submission_data(self,sid):
        submission = self.jotform_api_conn.get_submission(sid)
        return submission

    def get_submissions_data(self, formID, offset=None, limit=None, filterArray=None, order_by=None):
        submissions = self.jotform_api_conn.get_form_submissions(formID, offset, limit, filterArray, order_by)
        return submissions