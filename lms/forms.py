from django import forms
from django.contrib.auth.models import User
from .models import Course, Module, Lesson, Quiz, Question, Option, UserProfile


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Ismingiz",
                                 widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}))
    last_name = forms.CharField(max_length=50, required=True, label="Familiyangiz",
                                widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}))
    email = forms.EmailField(required=True, label="Email manzili",
                             widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}))
    role = forms.ChoiceField(choices=(('student', 'Talaba sifatida o\'qish'), ('teacher', 'O\'qituvchi sifatida dars o\'tish')),
                             label="Rolingiz",
                             widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none transition'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            role = self.cleaned_data.get('role', 'student')
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'level', 'duration_hours', 'short_description', 'description', 'thumbnail_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'level': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'short_description': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'rows': 5}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'placeholder': 'https://images.unsplash.com/...'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'pass_percentage']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'pass_percentage': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'order', 'video_url', 'duration_minutes', 'is_free_preview', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'video_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white font-mono', 'rows': 8}),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit_minutes', 'passing_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'rows': 3}),
            'time_limit_minutes': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'passing_score': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'points', 'explanation', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'rows': 3}),
            'points': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
            'explanation': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white'}),
        }
