# Test data section
section = u'flags'
# Backup_running
backup_running = u'backup_running'


def set_testdata_flag(flag, value):
    # TODO make better fix
    from webframework import TESTDATA
    try:
        TESTDATA[section][flag] = value
    except KeyError:
        TESTDATA.create_parameter(section, flag, value)


def get_testdata_flag(flag):
    # TODO make better fix
    from webframework import TESTDATA
    try:
        return TESTDATA[section][flag]
    except KeyError:
        return None