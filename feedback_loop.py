feedback_data = {}

def record_feedback(product_id, feedback_type):
    """Store user feedback"""
    if product_id not in feedback_data:
        feedback_data[product_id] = {"like": 0, "dislike": 0}

    feedback_data[product_id][feedback_type] += 1

def get_feedback(product_id):
    return feedback_data.get(product_id, {"like": 0, "dislike": 0})
