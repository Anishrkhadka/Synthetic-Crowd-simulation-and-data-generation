import numpy as np

try:
    from termcolor import cprint
except ImportError:
    cprint = None


def log_print(text, color=None, on_color=None, attrs=None):
    if cprint is not None:
        cprint(text, color=color, on_color=on_color, attrs=attrs)
    else:
        print(text)


def displayLog(InValue, InColor='green', attrs='bold'):
    log_print(InValue, color=InColor, attrs=[attrs])



def displayLog(InValue, InName=None, IsDisplayDataType=None,InColor='green', attrs='bold'):
    # if IsDisplayDataType:
    #     # -- if the InValue is dict -- #
    #     if type(InValue) is dict:
    #         for key, value in InValue.items():
    #             log_print(f"Key:{key} --Value:{value}", color=InColor, attrs=[attrs])
    #             # print()
    #
    #     # -- Any other type -- #
    #     else:
    #         log_print(type(InValue), color=InColor, attrs=[attrs])
    #         log_print(InValue, color=InColor, attrs=[attrs])
    #         # print(type(InValue))
    #         # print(InValue)
    #
    #
    # # -- Mainly for numpy array -- #
    # elif InName:
    #     # print(f"# -----{InName}-----#")
    #     log_print(f"# -----{InName}-----#", color=InColor, attrs=[attrs])
    #     try:
    #         log_print(f"Shape:{InValue.shape}", color='green', attrs=[attrs])
    #         # print("Shape:", InValue.shape)
    #     except:
    #         pass
    #     try:
    #         log_print((np.array2string(InValue).replace('[[', ' [').replace(']]', ']')),color=InColor, attrs=[attrs])
    #         # print(np.array2string(InValue).replace('[[', ' [').replace(']]', ']'))
    #     except:
    #         log_print(InValue, color=InColor, attrs=[attrs])
    #         # print(InValue)
    #         pass
    #     # try:
    #     #
    #     # except:
    #     #     pass
    #
    # else:
        log_print(f"{InValue}", color=InColor, attrs=[attrs])
        # print(f'# -----{InValue}-----#')
