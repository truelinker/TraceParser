import numbers
import pyparsing as pp
class EnumParseClass:
    
    def __init__(self):
        self.coreEnum = dict()
        self.msgMaskDict = dict()
        self.msgIdEnum = dict()
        
    
    def coreEnumParse(self):        
        
        _equal, _comma = map(pp.Suppress, "=,")
        matches = ["BASE", "NUM"]
    
        identifier = pp.Word(pp.printables)
        identifier2 = pp.Combine(pp.Word(pp.alphanums) + pp.OneOrMore('_' + pp.Word(pp.alphanums)))
        integer = pp.Word(pp.nums)
        
        _enumWithValue = identifier('enumName') + _equal + integer('enumValue') + _comma
        _enumNoValue = identifier2('enumName')
        
        with open('baseEnum.hpp','r') as sampleFile:
            lines = sampleFile.readlines();
            id = 0
            for line in lines:
                if any(x in line for x in matches):
                    try:
                        ret = _enumWithValue.parseString(line)
                    except:
                        ret = _enumNoValue.parseString(line)
                    print("Found : ", type(ret))
                    print("Found : ", ret.as_list())
                    print("Found : ", ret.as_dict())
                    print("type : ", type(id))
                    if 'enumValue' in ret:
                        id = int(ret['enumValue'])
                    else:
                        id += 1
                        ret['enumValue'] = id
                    print("Found : %s %d", ret['enumName'], ret['enumValue'])
                    self.coreEnum[ret['enumName']] = ret['enumValue']
                    print("dic length : ", len(self.coreEnum))
    
            return self.coreEnum
    def msgIdEnumParse(self):
    
        _equal = pp.Suppress('=')
        _comma = pp.Suppress(',')
        _lparenthesis = pp.Suppress('(')
        _rparenthesis = pp.Suppress(')')
        _or = pp.Suppress('|')
        _plus = pp.Suppress('+')
        _enum = pp.Suppress('enum')
        _ssmEnumId = pp.Suppress('type_t::')
        msgId = pp.Keyword("EnumId")
        _hex = pp.Keyword("0x00")
    
        self.msgMaskDict['ENUM_MASK'] = 0x9000
        self.msgMaskDict['ENUM_MASK1'] = 0xA000
        self.msgMaskDict['ENUM_MASK2'] = 0xB000
        self.msgMaskDict['ENUM_MASK3'] = 0x9200
        self.msgMaskDict['ENUM_MASK4'] = 0x9400
        self.msgMaskDict['ENUM_MASK5'] = 0x9600
        self.msgMaskDict['ENUM_MASK6'] = 0xA200
        self.msgMaskDict['ENUM_MASK7'] = 0xA400
        self.msgMaskDict['ENUM_MASK8'] = 0xA600
        self.msgMaskDict['ENUM_MASK9'] = 0xA800
        self.msgMaskDict['ENUM_MASK10'] = 0xB200
        self.msgMaskDict['ENUM_MASK11'] = 0xB400
    
        identifier = pp.Word(pp.alphanums)
        identifier2 = pp.Combine(pp.Word(pp.alphanums) + pp.OneOrMore('_' + pp.Word(pp.alphanums)))
        integer = pp.Word(pp.nums)
        hexNum = pp.Word(pp.hexnums)
    
        #EnumIdInvalid = 0,
        _enum = identifier('enumName') + _equal + integer('enumValue') + _comma
        # EnumId_A = type_t::ENUM_MASK,
        _enumMask = identifier2('enumName') + _equal + _ssmEnumId + identifier2('enumMask') + _comma
        #EnumIdPdsDeferredQueryResponse         =      type_t::ENUM_MASK10 + 1,
        _enumMask1 = identifier2('enumName') + _equal + _ssmEnumId + identifier2('enumMask') + _plus + integer('value') + _comma
        #EnumIdInitCore                         =     (type_t::ENUM_MASK1 | BASE_DATA1),
        _enumMask2 = identifier2('enumName') + _equal + _lparenthesis + _ssmEnumId + identifier2('enumMask') + _or + identifier2('enumMask2') + _rparenthesis + _comma
        #EnumIdInvalidRequest                  =     (type_t::ENUM_MASK11 | BASE_DATA1)
        _enumMask3 = identifier2('enumName') + _equal + _lparenthesis + _ssmEnumId + identifier2('enumMask') + _or + identifier2('enumMask2') + _rparenthesis
        #MsgGetAcmLCS,
        _enumNoValue = identifier2('enumName') + _comma
        #EnumIdRmtCmdInitializeReq               =     (type_t::ENUM_MASK11 ),
        _enumMask4 = identifier2('enumName') + _equal + _lparenthesis + _ssmEnumId + identifier2('enumMask') + _rparenthesis + _comma
        with open('enumIDs.hpp','r') as sampleFile:
            lines = sampleFile.readlines();
            id = 0
            for line in lines:
                if "EnumId" in line:
                    try:
                        ret = _enum.parseString(line)
                    except pp.ParseException:
                        try:
                            ret = _enumMask.parseString(line)
                        except pp.ParseException:
                            try:
                                ret = _enumMask1.parseString(line)
                            except pp.ParseException:
                                try:
                                    ret = _enumMask2.parseString(line)
                                except pp.ParseException:
                                    try:
                                        ret = _enumMask3.parseString(line)
                                        print("pass line : ", line)
                                    except pp.ParseException:
                                        try:
                                            ret = _enumNoValue.parseString(line)
                                            print("pass line : ", line)
                                        except pp.ParseException:
                                            try:
                                                ret = _enumMask4.parseString(line)
                                                print("pass line : ", line)
                                            except:
                                                print("Error line : ", line)
                                            finally:
                                                print("final line : ", line)
                                                pass
                    print("Found : ", type(ret))
                    print("Found : ", ret.as_list())
                    print("Found : ", ret.as_dict())
                    print("type : ", type(id))
                    if 'enumValue' in ret:
                        id = int(ret['enumValue'])
                    elif 'enumMask' in ret:
                        if 'value' in ret:
                            ret['enumValue'] = (int(self.msgMaskDict[ret['enumMask']]) + int(ret['value']))
                        elif 'enumMask2' in ret:
                            try:
                                ret['enumValue'] = (int(self.msgMaskDict[ret['enumMask']]) | int(self.coreEnum[ret['enumMask2']])) 
                            except KeyError:
                                ret['enumValue'] = 0xFFFFFFFF
                        else:
                            ret['enumValue'] = int(self.msgMaskDict[ret['enumMask']])                
                        if (ret['enumValue'] != 0xFFFFFFFF):
                            id = int(ret['enumValue'])
                    else:
                        id += 1
                        ret['enumValue'] = id
                    print("Found : %s %d", ret['enumName'], ret['enumValue'])
                    self.msgMaskDict[ret['enumName']] = int(ret['enumValue'])
                    print("dic length : ", len(self.msgMaskDict))
            
    
        for k, v in self.msgMaskDict.items():
            self.msgIdEnum[hex(v)] = k;
        return self.msgMaskDict
    
    def ConvertEnumIdToMsgStr(self,filteredFile,filteredWithMsgIDFile):
        _equal = pp.Suppress('=')
        
        matches = ["msgId", "EnumId&Param", "secondaryStatus "]
        identifier = pp.Keyword("EnumId&Param")
        identifier2 = pp.Keyword("EnumId")
        identifier3 = pp.Keyword("secondaryStatus")
        msgId = pp.Word(pp.alphanums)
        # EnumId&Param
        msgIDConvert = identifier("Message") + _equal + msgId("EnumId")
        # EnumId
        msgIDConvert2 = identifier2("Message") + _equal + msgId("EnumId")
        # secondaryStatus
        msgIDConvert3 = identifier3("Message") + _equal + msgId("EnumId")
        _outputfile = open(filteredWithMsgIDFile, "w")
        with open(filteredFile,'r') as filteredFile:
            lines = filteredFile.readlines();
            for line in lines:
                if any(x in line for x in matches):
                    try:
                        ret = msgIDConvert.searchString(line)[0]
                        print("Found : ", type(ret))
                        print("Found : ", ret.as_dict())
                        hexMsgID = int(ret[1], 16)
                        hexMsgID = hexMsgID >> 16
                        hexEnumIdTmp = hex(hexMsgID)
                        print("MessageId hex value : ", hexEnumIdTmp)
                    except:
                        try:
                            ret = msgIDConvert2.searchString(line)[0]
                            print("Found : ", type(ret))
                            print("Found : ", ret.as_dict())
                            hexMsgID = int(ret[1], 16)
                            hexEnumIdTmp = hex(hexMsgID)
                            print("MessageId hex value : ", hexEnumIdTmp)
                        except:
                            try:
                                ret = msgIDConvert3.searchString(line)[0]
                                print("Found : ", type(ret))
                                print("Found : ", ret.as_dict())
                                hexMsgID = int(ret[1], 16)
                                hexMsgID = hexMsgID >> 16
                                hexEnumIdTmp = hex(hexMsgID)
                                print("3MessageId hex value : ", hexEnumIdTmp)
                            except:
                                print(" error line : ", line)
                    
                    try:
                        _outputfile.write("=================================================== " + self.msgIdEnum[hexEnumIdTmp] + "(" + str(hexMsgID) + ")" + " " + hexEnumIdTmp + " " + " ============================\n")
                    except:
                        pass
                    
                _outputfile.write(line)
        _outputfile.close()
        
    def SecLibTraceConvert(self,filteredFile,filteredWithMsgIDFile):
        _equal = pp.Suppress('=')
        _colon = pp.Suppress(':')
        _lbroke = pp.Suppress('[')
        _rbroke = pp.Suppress(']')
        
        matches = ["msgId", "message"]
        
        identifier = pp.Keyword("msgId")
        identifier2 = pp.Keyword("message")
        identifier3 = pp.Keyword("message msgId")
        msgId = pp.Word(pp.alphanums)
        msgIDConvert = identifier("Message") + _colon + msgId("EnumId")
        msgIDConvert2 = identifier2("Message") + msgId("EnumId")
        msgIDConvert3 = identifier2("Message") + _colon + msgId("EnumId")
        msgIDConvert4 = identifier2("Message") + _colon + _lbroke + msgId("EnumId") + _rbroke
        msgIDConvert5 = identifier2("Message") + _lbroke + msgId("EnumId") + _rbroke
        msgIDConvert6 = identifier3("Message") + _colon + _lbroke + msgId("EnumId") + _rbroke
        _outputfile = open(filteredWithMsgIDFile, "w")
        with open(filteredFile,'r') as filteredFile:
            lines = filteredFile.readlines();
            for line in lines:
                if any(x in line for x in matches):
                    try:
                        ret = msgIDConvert.searchString(line)[0]
                        print("Found : ", type(ret))
                        print("Found : ", ret.as_dict())
                        hexMsgID = int(ret[1], 16)
                        hexEnumIdTmp = hex(hexMsgID)
                    except:
                        try:
                            ret = msgIDConvert2.searchString(line)[0]
                            print("Found : ", type(ret))
                            print("Found : ", ret.as_dict())
                            hexMsgID = int(ret[1], 16)
                            hexMsgID = hexMsgID >> 16
                            hexEnumIdTmp = hex(hexMsgID)
                            print("MessageId hex value : ", hexEnumIdTmp)
                        except:
                            try:
                                ret = msgIDConvert3.searchString(line)[0]
                                print("Found : ", type(ret))
                                print("Found : ", ret.as_dict())
                                hexMsgID = int(ret[1], 16)
                                hexMsgID = hexMsgID >> 16
                                hexEnumIdTmp = hex(hexMsgID)
                                print("MessageId hex value : ", hexEnumIdTmp)    
                            except:
                                try:
                                    ret = msgIDConvert4.searchString(line)[0]
                                    print("Found : ", type(ret))
                                    print("Found : ", ret.as_dict())
                                    hexMsgID = int(ret[1], 16)
                                    hexMsgID = hexMsgID >> 16
                                    hexEnumIdTmp = hex(hexMsgID)
                                    print("MessageId hex value : ", hexEnumIdTmp) 
                                except:
                                    try:
                                        ret = msgIDConvert5.searchString(line)[0]
                                        print("Found : ", type(ret))
                                        print("Found : ", ret.as_dict())
                                        hexMsgID = int(ret[1], 16)
                                        hexMsgID = hexMsgID >> 16
                                        hexEnumIdTmp = hex(hexMsgID)
                                        print("MessageId hex value : ", hexEnumIdTmp) 
                                    except:
                                        try:
                                            ret = msgIDConvert6.searchString(line)[0]
                                            print("Found : ", type(ret))
                                            print("Found : ", ret.as_dict())
                                            hexMsgID = int(ret[1], 16)
                                            #hexMsgID = hexMsgID >> 16
                                            hexEnumIdTmp = hex(hexMsgID)
                                            print("MessageId hex value : ", hexEnumIdTmp) 
                                            print("Error line : ", line)
                                        except:
                                            pass    
                                        finally:
                                            pass
                    
                    print("line : ", line)
                    try:
                        _outputfile.write("=================================================== " + self.msgIdEnum[hexEnumIdTmp] + "(" + str(hexMsgID) + ")" + " " + hexEnumIdTmp + " " + " ============================\n")
                    except:
                        pass
                    
                _outputfile.write(line)
        _outputfile.close()
                    