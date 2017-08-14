import urllib.request, json
import time


class TempClass:
    def __init__(self):
        pass

    def fill_data_to_file(self, file_name, tx_timestamp, inputs, outputs):

        file = open(file_name, "a")
        for inp_addr in inputs:
            for out_addr, amount in outputs.items():
                # print(str(tx_timestamp) + ";" + inp_addr + ";" + out_addr + ";" + str(amount))
                file.write(str(tx_timestamp) + ";" + inp_addr + ";" + out_addr + ";" + str(amount) + "\n")

    def get_tx_info_by_(self, tx_hash):
        try:
            with urllib.request.urlopen("https://bitaps.com/api/transaction/" + tx_hash) as url:
                data = json.loads(url.read().decode())
        except urllib.error:
            print("URL request error occurred in tx_hash: " + tx_hash)

        tx_timestamp = data['timestamp']
        inputs = []
        outputs = {}
        for addr in data['input']:
            inputs.append(addr['address'][0])
        for addr in data['output']:
            outputs[addr['address'][0]] = addr['amount']

        # for inp_addr in inputs:
        #    for out_addr, amount in outputs.items():
                # print(str(tx_timestamp) + ";" + inp_addr + ";" + out_addr + ";" + str(amount))

        # print("Stop test log message")
        output_file_name = 'transactions_info_outputs.txt'
        self.fill_data_to_file(output_file_name, tx_timestamp, inputs, outputs)

    def get_blocks_info_form_blockchain_info(self):
        # print(format(part, '02d'))
        part = 1
        file = open("blocks_timestamps_" + format(part, '02d') + ".txt", "w+")

        for i in range(460000, 479000):
            # range blocks is [460000, 478999], both sides included
            if (i % 100 == 0):
                print("Getting timestamp for block number " + str(i))

            # getting timestamp from JSON
            try:
                with urllib.request.urlopen("https://blockchain.info/block-index/" + str(i) + "?format=json") as url:
                    data = json.loads(url.read().decode())
                # extracting timestamps for block_ids
                t_stamp = str(data['time'])
            except urllib.error.HTTPError:
                t_stamp = None

            # writing timestamps to file
            file.write(str(i) + ";" + str(t_stamp) + "\n")

            # creating sliced files
            if (i % 1000 == 0 and i != 460000):
                file.close()
                part += 1
                file = open("blocks_timestamps_" + format(part, '02d') + ".txt", "w+")

            # trying to avoid API block
            time.sleep(.51)

        file.close()


if __name__ == '__main__':

    var = TempClass()
    # var.get_tx_info_by_("dbaadcf2e26c7565e44f66571479dd2269d5de1746460171fd84a8d87eff921a")
    # var.get_tx_info_by_("176fd34860252cda9677932002346557e5fcde91e6b7a916627a7c28b7421b1a")

    input_file_name = 'transactions_info_inputs.txt'


    with open(input_file_name) as f:
        content = f.readlines()
    f.close()

    i = 0
    for x in content:
        if (i == 5):
            break
        tx_hash = x.split(';')[1]
        print(tx_hash)
        var.get_tx_info_by_(tx_hash)
        time.sleep(0.51)
        i += 1

