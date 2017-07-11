#!/usr/bin/env python

import logging
import json
import time
import tornado.ioloop
import tornado.web
import tornado.escape

from tornado.options import define, options, parse_command_line
from encoder import Model as SentimentModel

define("port", default=5000, help="server port", type=int)
define("debug", default=False, help="enable debug mode")

class HealthCheckHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.finish()

class PredictSentimentHandler(tornado.web.RequestHandler):
    def initialize(self, sentiment_model):
        self.model = sentiment_model

    @tornado.web.asynchronous
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        messages = data['messages']
        ids = [message['id'] for message in messages]
        texts = [message['text'] for message in messages]

        start = time.time()
        predictions = self.model.transform(texts)
        logging.info('[sentiment] inference took %fs', time.time() - start)

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
    sentiment_model.transform([''])
    context = {
        "sentiment_model": sentiment_model,
    }

    routes = [
        (r"/health", HealthCheckHandler),
        (r"/sentiment/predict", PredictSentimentHandler, context),
    ]

    app = tornado.web.Application(
        routes,
        xsrf_cookies=False,
        debug=options.debug
    )

    app.listen(options.port)
    logging.info('[server] listening on port %s', str(options.port))
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
