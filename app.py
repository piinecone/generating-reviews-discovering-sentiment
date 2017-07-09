#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.options import define, options, parse_command_line
from encoder import Model as SentimentModel
import json

define("port", default=5000, help="server port", type=int)
define("debug", default=False, help="enable debug mode")

class PredictSentimentHandler(tornado.web.RequestHandler):
    def initialize(self, sentiment_model):
        self.model = sentiment_model

    @tornado.web.asynchronous
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        messages = data['messages']
        ids = [message['id'] for message in messages]
        texts = [message['text'] for message in messages]
        predictions = self.model.transform(texts)

        results = []
        for i in range(len(texts)):
            sentiment = predictions[i, 2388]
            results.append({
                'id': str(ids[i]),
                'text': str(texts[i]),
                'prediction': str(sentiment)
            })

        self.write(json.dumps(results))
        self.finish()

def main():
    parse_command_line()

    sentiment_model = SentimentModel()
    context = {
        "sentiment_model": sentiment_model,
    }

    routes = [
        (r"/sentiment/predict", PredictSentimentHandler, context),
    ]

    app = tornado.web.Application(
        routes,
        xsrf_cookies=False,
        debug=options.debug
    )

    app.listen(options.port)
    print('[server] listening on port', options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
