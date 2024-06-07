def get_i_data(req):
    i_data = req.args.to_dict()
    if (req.method == 'POST'):
        i_data = req.get_json()
    return i_data
