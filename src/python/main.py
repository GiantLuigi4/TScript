from python import method_loader


# Here's how you call a method from python
method_built = method_loader.load_or_get("Caller.tscript")
method_built.execute()
