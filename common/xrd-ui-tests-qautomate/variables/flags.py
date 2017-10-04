from webframework import TESTDATA

# Test data section
section = u'flags'
# Backup_running
backup_running = u'backup_running'


def set_testdata_flag(flag, value):
    try:
        TESTDATA[section][flag] = value
    except KeyError:
        TESTDATA.create_parameter(section, flag, value)
    print TESTDATA

def get_testdata_flag(flag):
    try:
        return TESTDATA[section][flag]
    except KeyError:
        return None