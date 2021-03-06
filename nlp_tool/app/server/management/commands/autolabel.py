from django.core.management.base import BaseCommand, CommandError
from server.models import (Document, Project, Label,
                          SequenceAnnotation, User)
import string

# if we want to add new labels, decide on some new colors for them
SOME_COLORS_TO_CHOOSE_FROM = ["#001f3f", "#0074D9", "#7FDBFF",
                              "#39CCCC", "#3D9970", "#2ECC40",
                              "#01FF70", "#FFDC00", "#FF4136",
                              "#FF851B", "#85144b", "#B10DC9",
                              "#111111"]

def get_new_shortcut(proj_id):
    """
    Since (project_id, shortcut_key) must be unique for a set of labels,
    we need to check what's taken and pick a unique shortcut key if we want
    to add a new label
    """
    labels = Label.objects.filter(project_id=proj_id)
    existing = set([label.shortcut for label in labels])
    kc = set(string.ascii_lowercase)
    diff = kc - existing
    return list(diff)[0]


def load_model(model_str):
    """
    Loads a model given an input string (could work differently)
    """
    if model_str == "en_core_web_md":
        import en_core_web_md
        model_func = en_core_web_md.load()
    if model_str == "en_resume_model":
        import en_resume_model
        model_func = en_resume_model.load()

    if model_str == "seed_data":
        import spacy
        from spacy.matcher import PhraseMatcher
        from spacy.tokens import Span

        class EntityMatcher(object):
            """
            Matcher with multi-case
            """
            def __init__(self, nlp, terms, label):
                patterns = [nlp(text.lower()) for text in terms]
                patterns += [nlp(text.upper()) for text in terms]
                patterns += [nlp(text.title()) for text in terms]
                self.matcher = PhraseMatcher(nlp.vocab)
                self.matcher.add(label, None, *patterns)
                self.name = '{}_matcher'.format(label)
        
            def __call__(self, doc):
                matches = self.matcher(doc)
                for match_id, start, end in matches:
                    span = Span(doc, start, end, label=match_id)
                    doc.ents = list(doc.ents) + [span]
                return doc

        nlp = spacy.load('en_core_web_md', disable=['ner'])
        with open("../data/seeds.json", 'r') as f:    
            seed_data_json = json.loads(f.read())
        for key in seed_data_json.keys():
            terms = seed_data_json[key]
            #terms = spacy_similarity(terms, nlp, num_similar=2)
            entity_matcher = EntityMatcher(nlp, terms, key)
            nlp.add_pipe(entity_matcher)
        model_func = nlp
    return model_func


class Command(BaseCommand):
    help = 'Loads a model and labels all documents in a given project'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)
        parser.add_argument('model_str', default='en_core_web_md')

    def handle(self, *args, **options):
        """
        Loads a model, gets all documents in the given project, and calls that
        model on each document. Optionally, it can create new labels for
        entities that it finds that don't exist in your project.
        """
        project_id = options['project_id']
        model_str = options['model_str']
        user = User.objects.get(username='admin')
        print("loading model")
        nlp_model = load_model(model_str)
        print("model loaded")
        project = Project.objects.get(pk=project_id)
        docs = Document.objects.filter(project_id=project_id)
#        docs = docs[:20]#
        
        # keep track of next label color, next label shortcut
        labels_created = 0
        next_color = SOME_COLORS_TO_CHOOSE_FROM[labels_created]
        next_short = get_new_shortcut(project_id)
        for doc in docs:
            parsed = nlp_model(doc.text)
            print(doc.text)
            if hasattr(doc, 'pk'):
                print(doc.pk)
            for ent in parsed.ents:
                elabel = ent.label_
                print(elabel)
                estart = ent.start_char
                eend = ent.end_char
                proj_label, created = Label.objects.get_or_create(text=elabel,
                                                                  project=project,
                                                                  defaults={'background_color': next_color,
                                                                            'shortcut': next_short})
                # keep track of next label color, next label shortcut
                if created:
                    labels_created = (labels_created + 1) % len(SOME_COLORS_TO_CHOOSE_FROM)
                    next_color = SOME_COLORS_TO_CHOOSE_FROM[labels_created]
                    next_short = get_new_shortcut(project_id)
                seq_ann_args = dict(document=doc, user=user, 
                                    label=proj_label, start_offset=estart,
                                    end_offset=eend, manual=False)
                ann, c = SequenceAnnotation.objects.get_or_create(**seq_ann_args)

