from flask import Flask, render_template, request, redirect, jsonify, abort, Response
import boto3
import os

app = Flask(__name__, static_url_path='/static', static_folder='web/static', template_folder='web/templates')

s3_client = boto3.client(
    's3',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        try:
            starting_token = request.args['next']
        except Exception as e:
            starting_token = None
        response = paginator.paginate(
            Bucket='bg-images-azura',
            Prefix='762x1100',
            EncodingType='url',
            PaginationConfig={
                'MaxItems': 100,
                'PageSize': 100,
                'StartingToken': starting_token
            }
        )
        response = [data for data in response][0]
        return render_template('index.html', response=response)
    except Exception as e:
        return jsonify({
            'status': False,
            'response': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)