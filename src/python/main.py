from python import method_loader

# Here's how you call a method
method_built = method_loader.load_or_get("ExampleMain.tscript")
method_built.execute()
