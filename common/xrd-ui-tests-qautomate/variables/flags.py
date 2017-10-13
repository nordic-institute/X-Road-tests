from webframework import TESTDATA

section = u'flags'
restore_backup = u'restore_backup'


def set_testdata_flag(flag, value):
    try:
        TESTDATA[section][flag] = value
    except KeyError:
        # TODO find better fix
        try:
            TESTDATA.create_parameter(section, flag, value)
        except AttributeError:
            pass



def get_testdata_flag(flag):
    try:
        return TESTDATA[section][flag]
    except KeyError:
        return None