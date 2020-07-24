from src import method_loader

# unbuiltClassDict = {
#     "Object": {
#     },
#     "Field": {
#         "inherits": "Object",
#         "fields": {
#             "val": 0
#         },
#         "Methods": {
#             "getValue": {
#                 "returns": "Object",
#                 "run": ["return val"]
#             },
#             "setValue": {
#                 "args": {
#                     "Object": "newVal"
#                 },
#                 "run": ["val=newVal"]
#             }
#         }
#     },
#     "TestObject": {
#         "inherits": "Object",
#         "Methods": {
#             "main": {
#                 "args": {
#                     "args": "String[]"
#                 },
#                 "run": [
#                     "say:\'hi\'",
#                     "ifGoto>0:rand || rand",
#                     "waitSeconds:1",
#                     "goto:0"
#                 ]
#             }
#         }
#     }
# }

# test_method = [
#     # "sayAndParse:time:execution.nano",
#     "ifGoto>3:rand",
#     "   exit:rand=0,128",
#     "goto:0",
#     "   say:'condition is false'",
#     "goto:0"
# ]

# method_built = method_builder.build("test_method", test_method)
method_built = method_loader.load_or_get("test1.tscript")

method_built.execute()

# objectDict = {
#     "ox00": {
#         "class": "Object"
#     },
#     "ox01": {
#         "class": "TestObject"
#     }
# }

# (class_builder.build(name="TestObject", data=unbuiltClassDict["TestObject"])).run_method(name="main")

# print(class_builder.build(name="TestObject", data=unbuiltClassDict["TestObject"]))
