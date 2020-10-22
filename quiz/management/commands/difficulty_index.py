

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Course
from quiz.models import Quiz, Question, QuizAttemptResponse


class Command(BaseCommand):
    help = 'Generates the difficulty index for each question in the given quiz'
    
    def add_arguments(self, parser):

        # Required quiz digest argument
        parser.add_argument(
            'digest',
            help='quiz digest',
            type=str,
            nargs='?',
        )
    
    def handle(self, *args, **options):
        digest = options['digest']
        
        # get the quiz
        try:
            quiz = Quiz.objects.get(quizprops__name='digest', quizprops__value=digest)
        except Quiz.DoesNotExist:
            print(commands.TERMINAL_COLOUR_WARNING)
            print(_(u"Quiz digest not found"))
            print(commands.TERMINAL_COLOUR_ENDC)
            return
        
        course = Course.objects.get(section__activity__digest=digest)
        print(course)
        print(quiz)
        
        # get the questions (in order)
        questions = Question.objects.filter(quizquestion__quiz=quiz)
       
        # loop to generate difficulty index for each question
        for question in questions:
            print(question.get_title("en"))
            qars = QuizAttemptResponse.objects.filter(question=question, quizattempt__user__is_staff=False)
            total_responses = qars.count()
            total_correct_responses = qars.filter(score__gt=0).count()
            difficulty_index = total_correct_responses/total_responses
            print(_(u"Difficulty Index: %0.2f") % difficulty_index)
            if difficulty_index > 0.90:
                print(commands.TERMINAL_COLOUR_WARNING)
                print(_(u"This question might be too easy for users"))
                print(commands.TERMINAL_COLOUR_ENDC)
                
            if difficulty_index < 0.30:
                print(commands.TERMINAL_COLOUR_WARNING)
                print(_(u"This question might be too difficult for users"))
                print(commands.TERMINAL_COLOUR_ENDC)
                
            print("\n")
        
        