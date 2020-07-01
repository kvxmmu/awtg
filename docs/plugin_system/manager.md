# AWTG plugin management system

definitions:
```text
Manager(default_filters=None):
    default filters - filters that manager will apply to all handlers
    
    import_plugin(plugin_module):
        just retrieving and loading exports attribute from module(duck typing, do anything you want with this feature) to handlers list
    
    import_handler(handler):
        appending your handler to handlers list

    import_plugin_module(package_name):
        Method that will import module by its package name and call import_plugin method

    import_plugins(plugins):
        Method that gets a list of modules and performing import_plugin on each

    __call__(message):
        just callback for messages/callback queries, go to source code to see how it works

async_decorator(*filters, optional=True):
    filters - input filters for handler 
    optional - if optional is False, all plugins must pass its not optional filters
    

AsyncHandler(handler):
    __optional__ - handler is optional or not

    is_optional(handler):
        returns handler.__optional__

    set_optional(optionality_status) -> self:
        setting __optional__ field to optionality_status

    add_filter(filter_) -> self:
        appending filter_ to filters list

    add_filters(*filters) -> self:
        extending filters list

    copy() -> copy of self object:
        returns AsyncHandler object copy

    __call__(message):
        same as in Manager

```

