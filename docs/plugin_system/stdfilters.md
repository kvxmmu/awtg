# AWTG standart filters

Split:
```text

Split(*pattern, case_sensitive=False,
      minimal_match_rate=None, custom_error_handler=None,
      error_fill=None, split_by=' ',
      error_generation_prefix=None, generate_error_message=True,
      error_send_function=None, strip_words=True,
      variants_separator='|'):
    pattern - tuple with text/set/list/tuple patterns,
              example: 'test', None, 'get', 'value'.
              is same as: strings[0] == 'test' and strings[2] == 'get' and strings[3] == 'value'
              None values are placed in split_extracted message memory field

    minimal_match_rate - for error generation, minimal number of pattern inconsistencies,
                         by default its len(pattern) - pattern.count(None)
    error_fill - error field description, used in error generation
    split_by - split user text by given pattern
    generate_error_message - perform error message generation when the number of inconsistencies reaches minimal_error_rate
    error_send_function - function that sends the error message, is invoked when error message is generated
    strip_words - remove pattern words from message text
    variants_separator - for error generation, separator for joining pattern strings

    passes:
        if message text coincides to pattern 

Command(*command_aliases, case_sensitive=False,
        strip=True):
    command_aliases - basic telegram commands, example: /command, /command@YourBot
    strip - remove command from source text

Prefix(regex, strip=True,
       case_sensitive=False):
    regex - prefix regex
    strip - remove prefix from source text
    case_sensitive - self-explanatory
    
    passes:
        if message text starts with prefix

RegularExpression(expr, match_type="match",
                  flags=0):
    expr - regular expression
    match_type - method for compiled regular expression
    flags - regular expression flags

    passes:
        if least one match found at message text 


```

Callback filters:
```text
AWTG providing simple RPC protocol for callback buttons, here explained RPC filters:

Filters:
    CustomJsonRPC(procedure_name) - json rpc with scheme:
        {
            "procedure": procedure_name,
            "args": {
                // data
            }
        }
        
        args are placed in args memory field
    
    CustomBinRPC(procedure_name) - binary rpc scheme
        go check doc string for format description
    
        binary data is encoded with base64 algorithm
    
        Available types:
          1) bytes
          2) str
          3) int(value no more than 2^32/2)
          4) dict (nested)

Builders:
    build_cjsonrpc_procedure(procedure_name, **args) -> custom json rpc string
    build_cbinrpc_procedure(procedure_name, **args) -> custom binary rpc string encoded with base64



```
