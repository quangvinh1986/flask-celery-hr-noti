from flask import Flask, g, render_template, send_from_directory, current_app, request, jsonify, redirect,url_for


def configure_route(app):
    @app.route('/download/<filename>')
    # @valid_required
    def download(filename):
        # print("DownloadFile", filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    @app.route('/myApi/hello', methods=['GET', 'POST'])
    def hook():
        if request.method == 'GET':
            return "Hello world!"
        else:
            return jsonify(message="unknow")

    # @app.route('/myApi/', methods=['GET', 'POST'])
    # def hello():
    #     if request.method == 'GET':
    #         # http://127.0.0.1:5001/myApi/swagger.json
    #         return "Hello world!"
    #     else:
    #         return jsonify(message="unknow")
    #
    # @app.route('/myApi/lib', methods=['GET', 'POST'])
    # def redirect():
    #     if request.method == 'GET':
    #         return redirect(url_for("myApi/swagger.json"))
    #         # http://127.0.0.1:5001/myApi/swagger.json
    #         # return "Hello world!"
    #     else:
    #         return jsonify(message="unknow")
