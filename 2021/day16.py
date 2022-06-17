class bits:
    command = ""
    packet_version = 0
    type_id = 0
    value = 0

    length_type_id = 0
    total_length_of_bits = 0
    number_of_sub_packets = 0
    data = ""
    parsed = 0
    sub_packets = []


    def __init__(self, command=""):
        self.command = command
        self.packet_version = int(self.command[0:3],2)
        self.type_id = int(self.command[3:6],2)

        if self.type_id == 4: #literal value
            temp = ""
            i = 6
            while i < len(command):
                more = int(self.command[i])
                a = self.command[i+1:i+5]
                temp += a
                if more == 0:
                    self.parsed = i+5
                    break
                i+=5
                
            #print(temp)
            self.value = int(temp,2)
        
        else: #operator packet
            self.length_type_id = int(self.command[6])
            if self.length_type_id == 0:
                self.total_length_of_bits = int(self.command[7:7+15],2)
                self.data = self.command[7+15:7+15+self.total_length_of_bits]
                bits_parsed = 0
                if self.total_length_of_bits > 0:
                    s = parsePacket(self.data)
                    self.sub_packets.append(s)
                    bits_parsed += s.parsed
                    while bits_parsed < self.total_length_of_bits:
                        s = parsePacket(s.command[s.parsed:])
                        self.sub_packets.append(s)
                        bits_parsed += s.parsed
                    
                    #print("left",len(s.command[s.parsed:]))
                    
                        
            else:
                self.number_of_sub_packets = int(self.command[7:7+11],2)
                self.data = self.command[7+11:]
                bits_parsed = 0
                if self.number_of_sub_packets > 0:
                    s = parsePacket(self.data)
                    self.sub_packets.append(s)
                    bits_parsed += s.parsed
                    while len(s.sub_packets) < self.number_of_sub_packets:
                        s = parsePacket(s.command[s.parsed:])
                        self.sub_packets.append(s)
                        bits_parsed += s.parsed

               
    def __str__(self):
        #return f"{self.command}\nPacket ver:\t{self.packet_version}\nType ID:\t{self.type_id}\nValue:\t\t{self.value}\nlength id:\t{self.length_type_id}\ntotal length of bits {self.total_length_of_bits}\nNumber of subpackets: {self.number_of_sub_packets}\ndata: {self.data}"
        return f"{self.command}\nPacket ver:\t{self.packet_version}\nType ID:\t{self.type_id}\nValue:\t\t{self.value}\n"

def hex2bin(input):
    hsize = len(input)*4
    return((bin(int(input,16))[2:]).zfill(hsize))

def parsePacket(input):
    return bits(input)

def part1(input):
    
    b = parsePacket(hex2bin(input))
    print(b)
    print("---------")
    total = b.packet_version
    x = 1
    for s in b.sub_packets:
        print("SUB_PACKET",x)
        x += 1
        print(s)
        
    print("total",total)
    #left_to_parse = b.total_length_of_bits
    #if left_to_parse > 0:
    #    temp = parsePacket(b.data)
    #    print(temp)
    


part1("D2FE28") #6
#part1("38006F45291200")
#part1("EE00D40C823060")
#part1("8A004A801A8002F478") #16 good
#part1("620080001611562C8802118E34") #12 #wrong answer
#part1("C0015000016115A2E0802F182340") #23 #runs forever
#part1("A0016C880162017C3686B18A3D4780") #31 #runs forever
#part1("420D598021E0084A07C98EC91DCAE0B880287912A925799429825980593D7DCD400820329480BF21003CC0086028910097520230C80813401D8CC00F601881805705003CC00E200E98400F50031801D160048E5AFEFD5E5C02B93F2F4C11CADBBB799CB294C5FDB8E12C40139B7C98AFA8B2600DCBAF4D3A4C27CB54EA6F5390B1004B93E2F40097CA2ECF70C1001F296EF9A647F5BFC48C012C0090E675DF644A675DF645A7E6FE600BE004872B1B4AAB5273ED601D2CD240145F802F2CFD31EFBD4D64DD802738333992F9FFE69CAF088C010E0040A5CC65CD25774830A80372F9D78FA4F56CB6CDDC148034E9B8D2F189FD002AF3918AECD23100953600900021D1863142400043214C668CB31F073005A6E467600BCB1F4B1D2805930092F99C69C6292409CE6C4A4F530F100365E8CC600ACCDB75F8A50025F2361C9D248EF25B662014870035600042A1DC77890200D41086B0FE4E918D82CC015C00DCC0010F8FF112358002150DE194529E9F7B9EE064C015B005C401B8470F60C080371460CC469BA7091802F39BE6252858720AC2098B596D40208A53CBF3594092FF7B41B3004A5DB25C864A37EF82C401C9BCFE94B7EBE2D961892E0C1006A32C4160094CDF53E1E4CDF53E1D8005FD3B8B7642D3B4EB9C4D819194C0159F1ED00526B38ACF6D73915F3005EC0179C359E129EFDEFEEF1950005988E001C9C799ABCE39588BB2DA86EB9ACA22840191C8DFBE1DC005EE55167EFF89510010B322925A7F85A40194680252885238D7374C457A6830C012965AE00D4C40188B306E3580021319239C2298C4ED288A1802B1AF001A298FD53E63F54B7004A68B25A94BEBAAA00276980330CE0942620042E3944289A600DC388351BDC00C9DCDCFC8050E00043E2AC788EE200EC2088919C0010A82F0922710040F289B28E524632AE0") #63 is wrong