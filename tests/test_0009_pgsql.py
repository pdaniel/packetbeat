from pbtests.packetbeat import TestCase


class Test(TestCase):
    def test_select(self):
        self.render_config_template(
            pgsql_ports=[5432]
        )
        self.run_packetbeat(pcap="pgsql_request_response.pcap")

        objs = self.read_output()
        assert len(objs) == 1
        o = objs[0]
        assert o["type"] == "pgsql"
        assert o["method"] == "SELECT"
        assert o["query"] == "select * from test"
        assert o["response_raw"] == "a,b,c\nmea,meb,mec\nmea1," + \
            "meb1,mec1\nmea2,meb2,mec2\nmea3,meb3,mec3\n"
        assert o["bytes_out"] == 202

    def test_insert(self):
        self.render_config_template(
            pgsql_ports=[5432]
        )
        self.run_packetbeat(pcap="pgsql_insert.pcap")

        objs = self.read_output()
        assert len(objs) == 1
        o = objs[0]
        assert o["type"] == "pgsql"
        assert o["method"] == "INSERT"
        assert o["bytes_out"] == 16

    def test_insert_error(self):
        self.render_config_template(
            pgsql_ports=[5432]
        )
        self.run_packetbeat(pcap="pgsql_insert_error.pcap")

        objs = self.read_output()
        assert len(objs) == 1
        o = objs[0]
        assert o["type"] == "pgsql"
        assert o["method"] == "INSERT"
        assert o["status"] == "Error"
        assert o["pgsql.error_code"] == "23505"
        assert o["pgsql.iserror"] is True
