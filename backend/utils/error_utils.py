def handle_errors(error_list, caller_name):
    print(f"[{caller_name}] validation errors occurred:")
    for error in error_list:
        print(f"\t{error_list[error]}")