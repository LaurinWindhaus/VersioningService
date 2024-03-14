def get_diff(old_json, new_json):
    diff = []
    try:
        for key in new_json:
            if key in old_json:
                if new_json[key] != old_json[key]:
                    diff.append({"column": key, "old_value": old_json[key], "new_value": new_json[key]})
            else:
                diff.append({"column": key, "old_value": None, "new_value": new_json[key]})
        for key in old_json:
            if key not in new_json:
                diff.append({"column": key, "old_value": old_json[key], "new_value": None})
    except Exception as e:
        print(f"An error occurred: {e}")
    return diff


def rollback_to_version(current_json: dict, changes: dict, current_version: int, target_version: int):
    if target_version < 0 or target_version > current_version:
        return None
    
    rolled_back_json = current_json.copy()  # Make a copy of the current JSON object to avoid modifying it directly
    for change in reversed(changes):  # Iterate through changes in reverse order
        version = int(change['version'])
        if version > target_version:
            # Convert the json_data_changes string to a list of dictionaries
            change_data = eval(change['json_data_changes'])
            for change_item in change_data:
                column = change_item['column']
                old_value = change_item['old_value']
                new_value = change_item['new_value']
                # Revert the changes to the rolled_back_json
                if old_value is None:
                    rolled_back_json.pop(column, None)  # Remove the key if it was added
                else:
                    rolled_back_json[column] = old_value  # Revert to the old value
        else:
            break  # Stop iteration if we reach the target version or beyond
    return rolled_back_json


def update_to_version(current_json: dict, changes: dict, current_version: int, target_version: int):
    max_version = max(int(change['version']) for change in changes)
    if target_version < current_version or target_version > max_version:
        return None
    
    updated_json = current_json.copy()  # Make a copy of the current JSON object to avoid modifying it directly
    for change in changes:  # Iterate through changes
        version = int(change['version'])
        if version <= target_version:
            # Convert the json_data_changes string to a list of dictionaries
            change_data = eval(change['json_data_changes'])
            for change_item in change_data:
                column = change_item['column']
                old_value = change_item['old_value']
                new_value = change_item['new_value']
                # Update the JSON with the changes
                if new_value is None:
                    updated_json.pop(column, None)  # Remove the key if it was deleted
                else:
                    updated_json[column] = new_value  # Update to the new value
        else:
            continue  # Skip changes that are before the target version
    return updated_json


# old_json = {"name": "John", "age": 30, "city": "New York"}
# new_json = {"name": "John", "age": 31, "country": "USA"}
# very_new_json = {"name": "John", "age": 32, "country": "EUROPE", "city": "Berlin"}

# changes = [
#    {
#       "id":16,
#       "document_type":"verpackungsvorschrift",
#       "document_id":"1",
#       "version":"1",
#       "json_data_changes":"[{'column': 'age', 'old_value': 30, 'new_value': 31}, {'column': 'country', 'old_value': None, 'new_value': 'USA'}, {'column': 'city', 'old_value': 'New York', 'new_value': None}]",
#       "created_at":"2024-03-13 11:28:54.507000",
#       "created_by:":"laurinwindhaus@poeppelmann.com"
#    },
#    {
#       "id":17,
#       "document_type":"verpackungsvorschrift",
#       "document_id":"1",
#       "version":"2",
#       "json_data_changes":"[{'column': 'age', 'old_value': 31, 'new_value': 32}, {'column': 'country', 'old_value': 'USA', 'new_value': 'EUROPE'}, {'column': 'city', 'old_value': None, 'new_value': 'Berlin'}]",
#       "created_at":"2024-03-13 11:29:11.200000",
#       "created_by:":"laurinwindhaus@poeppelmann.com"
#    }
# ]

# current_json = {"name": "John", "age": 32, "country": "EUROPE", "city": "Berlin"}

# rolled_back_json = rollback_to_version(current_json, changes, 2, 0)
# print(rolled_back_json)
# rolled_back_json = rollback_to_version(current_json, changes, 2, 1)
# print(rolled_back_json)
# rolled_back_json = rollback_to_version(current_json, changes, 2, 2)
# print(rolled_back_json)

# current_json = {"name": "John", "age": 30, "city": "New York"}

# updated_json = update_to_version(current_json, changes, 0, 0)
# print(updated_json)
# updated_json = update_to_version(current_json, changes, 0, 1)
# print(updated_json)
# updated_json = update_to_version(current_json, changes, 0, 2)
# print(updated_json)