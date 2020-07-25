from python import method_loader


# Here's how you call a method from python
# method_built = method_loader.load_or_get("ExampleMain.tscript")
# method_built = method_loader.load_or_get("EqualsTest.tscr")
# method_built = method_loader.load_or_get("MarkersTest.tscr")
# method_built = method_loader.load_or_get("MarkersTwo.tscr")
method_built = method_loader.load_or_get("Variables.tscr")
# method_built = method_loader.load_or_get("GotoEndAndMoreOnComments.tscr")
method_built.execute()
