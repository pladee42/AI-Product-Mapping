class GetPrompt:
    def __init__(self, vendor_data : str, bzbs_data : str):
        self.vendor_data = vendor_data
        self.bzbs_data = bzbs_data
        self.prompt = f"""
                Here is the invoice data that is read from vendor invoice:
                -- VENDOR DATA STARTS HERE --

                {vendor_data}

                -- VENDOR DATA ENDS HERE --

                And, here is the product data from Buzzebees database:
                -- BUZZEBEES DATA STARTS HERE --

                {bzbs_data}

                -- BUZZEBEES DATA ENDS HERE --

                Please provide the matching result in JSON format.
                """

    def get_prompt(self, vendor_data, bzbs_data):
        self.prompt = f"""
                Here is the invoice data that is read from vendor invoice:
                -- VENDOR DATA STARTS HERE --

                {vendor_data}

                -- VENDOR DATA ENDS HERE --

                And, here is the product data from Buzzebees database:
                -- BUZZEBEES DATA STARTS HERE --

                {bzbs_data}

                -- BUZZEBEES DATA ENDS HERE --

                Please provide the matching result in JSON format.
                """

        return self.prompt