from googletrans import Translator

# translates content in an event log into a given language
def translate(event_log, lang_code):
    translator = Translator()

    # Looping through each trace\event in the log
    for trace in event_log:
        for event in trace:
            # Here we focus on the concept name i.e. the activity name
            if 'concept:name' in event:
                try:
                    translation = translator.translate(event['concept:name'], dest=lang_code)
                    event['concept:name'] = translation.text
                except Exception as e:
                    print(f"Translation error occured: {e}")
    return event_log