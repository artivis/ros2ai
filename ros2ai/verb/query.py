# Copyright 2023 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ros2ai.api import add_global_arguments
from ros2ai.api.openai import ChatCompletionClient, ChatCompletionClientStream
from ros2ai.verb import VerbExtension

class QueryVerb(VerbExtension):
    """Query a single completion to OpenAI API."""

    def add_arguments(self, parser, cli_name):
        # add global arguments
        add_global_arguments(parser)

        # sub-command arguments
        parser.add_argument(
            "questions", nargs="+", default=[],
            help="Multiple sentences separated by spaces, enclosed in double quotes.")
        parser.add_argument(
            '-s',
            '--stream',
            action='store_true',
            help='Prints using streaming responses')
        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='Prints detailed response information')

    def main(self, *, args):
        sentence = ''
        if (args.questions):
            sentence = " ".join(args.questions)
        if (sentence == ''):
            print('Dont be shy, put some questions! (I am not AI)') 
        
        if (args.stream is True):
            client = ChatCompletionClientStream(args)
            client.call(sentence)
            client.print_stream()
        else:
            client = ChatCompletionClient(args)
            client.call(sentence)
            if (args.verbose is True):
                client.print_all()
            else:
                client.print_content()
