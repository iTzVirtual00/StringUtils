# data, display text, icon, type (Plasma::QueryType), relevance (0-1), properties (subtext, category and urls)
def krunner_response(data, display, properties={}, icon="arrow-right-double", type=100, relevance=5.0):
    return data, display, icon, type, relevance, properties