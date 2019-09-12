# -*- coding: utf-8 -*-
#
#    This file belongs to the Interactive Syllabus project
#
#    Copyright (C) 2017  Alexandre Dubray, François Michel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.body import CodeBlock, Container
from docutils.statemachine import StringList

import docutils.parsers.rst.directives


def uri(argument):
    """
    Return the URI argument with whitespace removed.
    (Directive option conversion function.)
    Raise ``ValueError`` if no argument is found.
    """
    if argument is None:
        raise ValueError('argument required but none supplied')
    else:
        uri = ''.join(argument.split())
        return re.sub('^/assets/', '/syllabus/{{session["course"]}}/assets/', uri)


# Oh yeah baby!
docutils.parsers.rst.directives.uri = uri


def get_directives():
    return [('inginious', InginiousDirective),
            ('inginious-sandbox', InginiousSandboxDirective),
            ('table-of-contents', ToCDirective),
            ('author', AuthorDirective),
            ('teacher', TeacherDirective),
            ('framed', FramedDirective),
            ('print', PrintOnlyDirective)]


class InginiousDirective(Directive):
    """
    required argument: the task id on which post the answer on INGInious
    optional argument 1: the language mode supported by CodeMirror
    optional argument 2: the number of blank lines to display in print mode
    directive content: the prefilled code in the text area

    The directive will display the content in print mode if the "print" attribute is set to True in the session.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 2
    html = """
    <div class="inginious-task" style="margin: 20px" data-language="{3}">
        <div class="feedback-container" class="alert alert-success" style="padding: 10px;" hidden>
            <strong>Success!</strong> Indicates a successful or positive action.
        </div>
        <form method="post" action="{0}">
            <textarea style="width:100%; height:150px;" class="inginious-code" name="code">{1}</textarea><br/>
            <input type="text" name="taskid" class="taskid" value="{2}" hidden/>
            <input type="text" name="input" class="to-submit" hidden/>
        </form>
        <button class="btn btn-primary button-inginious-task" id="{2}" value="Submit">Soumettre</button>
    </div>

    """

    def get_html_content(self, sandbox):

        html_no_lti = """
        {{% set action_to_do = '/postinginious/' + session["course"] %}}
        {{% if not inginious_config['same_origin_proxy'] %}}
            {{% set action_to_do = inginious_course_url %}}
        {{% endif %}}
        <div class="inginious-task" style="margin: 20px" data-language={0}">
            <div class="feedback-container" class="alert alert-success" style="padding: 10px;" hidden>
                <strong>Success!</strong> Indicates a successful or positive action.
            </div>
            <form method="post" action="{{{{ action_to_do }}}}">
                <textarea style="width: 100%; height: 100%; height: 150px;" class="inginious-code" name="code">{1}</textarea><br/>
                <input type="text" name="taskid" class="taskid" value="{2}" hidden />
                <input type="text" name="input" class="to-submit" hidden />
            </form>
            <button class="btn btn-primary button-inginious-task" id="{2}" value="Submit">Soumettre</button>
        </div>
        """.format(self.arguments[2] if len(self.arguments) == 3 else "text/x-python",
                   '\n'.join(self.content),
                   self.arguments[0])

        html_lti = """
        {{% set user = session.get("user", None) %}}
        {{% if user is not none %}}
            {{% set data, launch_url = get_lti_data(course_str, logged_in["email"] if logged_in is not none else none, "{0}") %}}
            {{% set inputs_list = [] %}}
            {{% for key, value in data.items() %}}
                {{% set a = inputs_list.append('<input type="hidden" name="{{0}}" value="{{1}}" />'.format(key, value)) %}}
            {{% endfor %}}
            {{% set form_inputs = '\\n'.join(inputs_list) %}}
            <iframe name="myIframe{0}" frameborder="0" allowfullscreen"true" webkitallowfullscreen="true" mozallowfullscreen="true" scrolling="no"
                style="overflow: hidden; width: 100%; height: 520px" src=""></iframe>
            <form action="{{{{ launch_url }}}}"
                  name="ltiLaunchForm"
                  class="ltiLaunchForm"
                  method="POST"
                  encType="application/x-www-form-urlencoded"
                  target="myIframe{0}">
            {{{{ form_inputs|safe }}}}
            <button class="inginious-submitter" type="submit">Launch the INGInious exercise</button>
            </form>
        {{% else %}}
            <pre style="overflow: hidden; width: 100%; height: 520px">Please log in to see this exercise</pre>
        {{% endif %}}
        """.format(self.arguments[0])

        if sandbox:
            html_no_print = html_no_lti
        else:
            html_no_print = """
            {{% set use_lti = "lti" in inginious_config %}}
            {{% if use_lti %}}
                {0}
            {{% else %}}
                {1}
            {{% endif %}}
        """.format(html_lti, html_no_lti)

        # par = nodes.raw('', html, format='html')

        c = []
        n_blank_lines = int(self.arguments[1]) if len(self.arguments) >= 2 else 0
        c.append(
            '{%% set submission = get_lti_submission(course_str, logged_in["email"], "%s") if logged_in is not none else none %%}' %
            self.arguments[0])
        c.append("{% if submission is not none %}"
                 "{% for item in submission['question_answer'] %}"
                 "<div>"
                 "<div style='display: block; border: 1px solid #000000; padding: 5px; border-radius: 5px;'>"
                 "<b>Question:</b>"
                 "<br>"
                 "{{ render_rst_str(item['question'])|safe }}"
                 "<br>"
                 "<b>Answer {{'(correct)' if item['success'] else '(incorrect)'}} :</b>"
                 "<br>"
                 "<div style='font-family: Courier New, Courier'>"
                 "{{ render_rst_str(item['answer'], type=item['type'])|safe }}"
                 "</div> "
                 "</div>"
                 "</div>"
                 "<br>"
                 "{% endfor %}"
                 "{% endif %}")
        c.append("{% if submission is none %}"
                 "<pre>")
        if self.content:
            c.append("%s" % "\n".join(list(self.content)))
        c.append("{%% for i in range(%d) %%}"
                 "{{ '\n' }}"
                 "{%% endfor %%}"
                 "{%% endif %%}"
                 "</pre>" % n_blank_lines)
        html_print = "\n".join(c)

        html = """
        {{% if not session.get("print_mode", False) %}}
        {}
        {{% else %}}
        {}
        {{% endif %}}
        """.format(html_no_print, html_print)

        par = nodes.raw('', html, format='html')
        return [par]

    def run(self):
        return self.get_html_content(False)


class InginiousSandboxDirective(InginiousDirective):
    def run(self):
        return self.get_html_content(True)


class ToCDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    html = """
    <div id="table-of-contents">
        <h2> Table des matières </h2>
    """

    def run(self):
        if len(self.arguments) == 1:
            # TODO: change this ugly part, rethink the chapter_index.rst completely :'(
            self.arguments[0] = "chapter_path" if self.arguments[0].replace(" ", "") == "{{chapter_path}}" else "%s" % \
                                                                                                                self.arguments[
                                                                                                                    0]
            self.html += "{%% set chapter = toc.get_chapter_from_path(%s) %%}" % self.arguments[0]
            self.html += "<h3> {{ chapter.title }} </h3>\n"
            self.html += self.parse()
        else:
            self.html += "{% set chapter = none %}"
            # for keys in toc.keys():
            #     self.html += "<h3> " + toc[keys]["title"] + "</h3>\n"
            #     self.html += self.parse(toc[keys]["content"], keys + "/")
            self.html += self.parse()
        return [nodes.raw(' ', self.html, format='html')]

    def parse(self):
        return """
        {% for content in (toc.get_top_level_content() if chapter is none else toc.get_direct_content_of(chapter)) recursive %}
            <ul>
                <li style="list-style-type: none;"><a href="/syllabus/{{ course_str }}/{{content.request_path}}">{{content.title}}</a></li>
                {% if "Chapter" in content.__class__.__name__ %}
                    {{ loop(toc.get_direct_content_of(content)) }}
                {% endif %}
            </ul>
        {% endfor %}
        """


class AuthorDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        html = '<div align=right><div style="display: inline-block;"><p><small> Auteur(s) : ' + self.content[
            0] + '</small></p>'
        html += '<hr style="margin-top: -5px;;" >\n'
        html += '</div></div>'
        return [nodes.raw(' ', html, format='html')]


class FramedDirective(Directive):
    """
    Creates a frame with the specified number of blank lines appended to the
    provided content if there is one.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        sl = StringList([" " for _ in range(int(self.arguments[0]))])
        if not self.content:
            self.content = sl
        else:
            self.content.append(sl)
        par = nodes.raw('',
                        """<pre style="background-color: #ffffff; border: 1px solid #000000">%s</pre>""" % "\n".join(
                            self.content), format='html')

        return [par]

class TeacherDirective(Directive):
    """
    The directive will wrap its content inside this Jinja template code :

    ```
    {% if logged_in is not none and logged_in["right"] == "admin" %}
        .. container:: framed

            content

    {% endif %}
    ```

    meaning that when rendered by Jinja, the content will only be displayed to the admin user.

    For this to work, il needs a variable named `user` containing the correct user.

    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        if self.content:
            sl = StringList(["{% if ((logged_in is not none) and (logged_in['right'] in ['admin', 'teacher'])) %}"])
            sl.append(StringList([""]))
            sl.append(StringList([".. container:: framed"]))
            sl.append(StringList([""]))
            new_content = StringList([])
            for item in self.content:
                new_content.append(StringList(["    %s" % item]))
            sl.append(new_content)
            sl.append(StringList([""]))
            sl.append(StringList(["{% endif %}"]))
            self.content = sl
        return Container(content=self.content, arguments=[], lineno=self.lineno,
                         block_text=self.block_text, content_offset=self.content_offset, name="container",
                         options=self.options, state=self.state, state_machine=self.state_machine).run()


class PrintOnlyDirective(Directive):
    """
    The directive will display its content only if it is in print mode

    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        content = """
            {{% if session.get("print_mode", True) %}}
                {}
            {{% endif %}}
        """.format(self.content)
        return Container(content=content, arguments=[], lineno=self.lineno,
                         block_text=self.block_text, content_offset=self.content_offset, name="container",
                             options=self.options, state=self.state, state_machine=self.state_machine).run()


def setup(app):
    for name, directive in get_directives():
        app.add_directive(name, directive)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
