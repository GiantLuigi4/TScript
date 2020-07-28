from python import method_loader


# method_built = method_loader.load_or_get("ExampleMain.tscript")
# method_built = method_loader.load_or_get("EqualsTest.tscr")
# method_built = method_loader.load_or_get("MarkersTest.tscr")
# method_built = method_loader.load_or_get("MarkersTwo.tscr")
# method_built = method_loader.load_or_get("Variables.tscr")
# method_built = method_loader.load_or_get("StringTest.tscr")
# method_built = method_loader.load_or_get("Inputs.tscr")
# method_built = method_loader.load_or_get("MarkersThree.tscr")
# method_built = method_loader.load_or_get("reload.tscr")
# method_built = method_loader.load_or_get("Test.tscr")
# method_built = method_loader.load_or_get("GotoEndAndMoreOnComments.tscr")


# Here's how you call a method from python
method_built = method_loader.load_or_get("SnakeGame.tscr")
method_built.execute()
