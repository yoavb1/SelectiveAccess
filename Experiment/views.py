# username: yoavbenyaakov
# password: YoavJoachim0571JyY
# email: yoavb1@mail.tau.ac.il
# python manage.py createsuperuser

# Condition 1 - Binary output
# Condition 2 - Conditional probability

# Order 1 - Not PD --> PD
# Order 2 - PD --> Not PD

import pandas as pd
import time
from django.shortcuts import render, redirect
from .models import *
import numpy as np
import random
import pandas as pd

# The function read from a csv file the experiment's parameters and return a parameters dictionary
def set_parameters():
    # param = pd.read_csv("/home/IWiTLab/IntegratedInformation/parameters/parameters.csv").rename(
    #     columns={'Unnamed: 0': 'parameter', '0': 'value'})
    param = pd.read_csv("parameters/parameters.csv").rename(columns={'Unnamed: 0': 'parameter', '0': 'value'})
    blocks = param[param['parameter'] == 'blocks']['value'].iloc[0]
    events = 5#int(param[param['parameter'] == 'events']['value'].iloc[0])
    test_events = 5#int(param[param['parameter'] == 'test_events']['value'].iloc[0]) + 1
    budget = int(param[param['parameter'] == 'budget']['value'].iloc[0])
    system_cost = round(param[param['parameter'] == 'system_cost']['value'].iloc[0], 1)
    v_tp = param[param['parameter'] == 'v_tp']['value'].iloc[0]
    v_fp = param[param['parameter'] == 'v_fp']['value'].iloc[0]
    v_fn = param[param['parameter'] == 'v_fn']['value'].iloc[0]
    v_tn = param[param['parameter'] == 'v_tn']['value'].iloc[0]
    param = {'B': blocks, 'N': events, 'N_test': test_events, 'budget': budget,
             'v_tp': v_tp, 'v_fp': v_fp, 'v_tn': v_tn, 'v_fn': v_fn, 'system_cost': system_cost}
    return param


def user_information(request):
    try:
        user_agent = request.user_agent
        is_mobile = request.user_agent.is_mobile
        is_tablet = request.user_agent.is_tablet
        is_pc = request.user_agent.is_pc
        is_bot = request.user_agent.is_bot
        return user_agent, is_mobile, is_tablet, is_pc, is_bot
    except:
        return '', '', '', '', ''


# The function get the participant's IP
def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ''
    return ip


def shuffle_events(data):
    shuffled_data = data[data['trial'] == 0].copy()
    blocks = [1, 2, 3, 4]
    for block in range(1, 5):
        block_number = random.choices(blocks)[0]
        blocks.remove(block_number)
        shuffle_block = data[data['block'] == block_number].sample(frac=1).copy().reset_index().\
            drop(['trial', 'index'], axis=1).reset_index().rename(columns={'index': 'trial'})
        shuffle_block['block'] = shuffle_block['block'].apply(lambda x: block)
        shuffled_data = pd.concat([shuffled_data, shuffle_block])
    shuffled_data['trial'] = shuffled_data['trial'].apply(lambda x: x + 1)
    return shuffled_data.sort_values(['block', 'trial'])


# The function return the events
def get_events():
    # df = pd.read_csv("/home/IWiTLab/IntegratedInformation/events/events.csv")
    df = pd.read_csv("events/events.csv")
    events = shuffle_events(df)
    events['P(Human)'] = events['P(Human)'].apply(lambda x: round(x,2))
    events['P(Low_System_Likelihood)'] = events['P(Low_System_Likelihood)'].apply(lambda x: round(x, 2))
    events['P(High_System_Likelihood)'] = events['P(High_System_Likelihood)'].apply(lambda x: round(x, 2))
    events['P(Low_System_Integrated)'] = events['P(Low_System_Integrated)'].apply(lambda x: round(x, 2))
    events['P(High_System_Integrated)'] = events['P(High_System_Integrated)'].apply(lambda x: round(x, 2))
    data = {}
    for index, row in events.iterrows():
        data[f"({row['block']},{row['trial']})"] = {'type': row['event'],
                                                    'P(Human)': row['P(Human)'],
                                                    'P(Low_System_Binary)': row['P(Low_System_Binary)'],
                                                    'P(High_System_Binary)': row['P(High_System_Binary)'],
                                                    'P(Low_System_Likelihood)': row['P(Low_System_Likelihood)'],
                                                    'P(High_System_Likelihood)': row['P(High_System_Likelihood)'],
                                                    'P(Low_System_Integrated)': row['P(Low_System_Integrated)'],
                                                    'P(High_System_Integrated)': row['P(High_System_Integrated)'],
                                                    'stimulus_h': row['stimulus_h'],
                                                    'stimulus_s_low': row['stimulus_s_low'],
                                                    'stimulus_s_high': row['stimulus_s_high']}
    return data


# Create your views here.
def registration(request):
    request.session['aid'] = request.GET.get('aid', 'Student')
    request.session['finish'] = False
    if request.method == "POST":
        if request.POST['Continue'] == 'Continue':
            user_agent, is_mobile, is_tablet, is_pc, is_bot = user_information(request)
            request.session['events'] = get_events()
            request.session['params'] = set_parameters()
            output = ['binary', 'likelihood', 'likelihood_integrated']
            request.session['output'] = random.choice(output)
            request.session['sensitivity'] = random.choice(['low', 'high'])
            request.session['condition'] = f"{request.session['output']}_{request.session['sensitivity']}"
            request.session['order'] = np.random.randint(2) + 1
            request.session['score'] = request.session['params']['budget']
            request.session['Information Button'] = True
            request.session['nasa_tlx_system'] = False
            request.session['instruction'] = 1
            request.session['warning'] = 1
            request.session['block'] = 1
            request.session['Previous Classification'] = ''
            p = Participant.objects.create(condition=request.session['condition'], aid=request.session['aid'],
                                           order=request.session['order'],
                                           user_agent=user_agent, is_pc=is_pc, is_mobile=is_mobile, is_tablet=is_tablet,
                                           is_bot=is_bot, ip=get_client_ip(request), finish=False)
            print(p)
            request.session['id'] = p.id
            p.save()
            return redirect('/consent_form/')
        if request.POST['Continue'] == 'End the experiment':
            return redirect('/end/')
    if request.method == "GET":
        return render(request=request,
                      template_name='Registration.html')


def consent_form(request):
    if request.method == "POST":
        if request.POST['Continue'] == 'Continue':
            return redirect('/instructions/')
        elif request.POST['Continue'] == 'End the experiment':
            return redirect('/end/')
        else:
            return redirect('/consent_form/')
    if request.method == "GET":
        return render(request=request,
                      template_name='ConsentForm.html')
    else:
        return redirect('/consent_form/')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def end(request):
    # if not request.user.is_authenticated:
    #     return redirect('/end/')
    try:
        participant_object = Participant.objects.filter(id=request.session['id']).first()
        participant_object.save()
        number_of_events = Events.objects.filter(participant=participant_object).count()
        number_of_nasa = Nasa.objects.filter(participant=participant_object).count()
        number_of_trust = Trust.objects.filter(participant=participant_object).count()
        if number_of_events == 200 and number_of_nasa == 2 and number_of_trust == 1:
            request.session['finish'] = True
        else:
            request.session['finish'] = False
        hours = (participant_object.end_time.hour - participant_object.start_time.hour) * 3600
        minutes = (participant_object.end_time.minute - participant_object.start_time.minute) * 60
        seconds = participant_object.end_time.second - participant_object.start_time.second
        experiment_time = hours + minutes + seconds
    except:
        request.session['finish'] = False
        experiment_time = 0

    Participant.objects.filter(id=request.session['id']).update(total_time=experiment_time,
                                                                finish=request.session['finish'])
    return render(request=request,
                  template_name='End.html', context={'finish': request.session['finish'], 'aid': request.session['aid']})


def instructions(request):
    if request.method == "POST":
        if request.POST['Continue'] == 'Continue':
            request.session['trial'] = 1
            if request.session['instruction'] == 1:
                request.session['instruction'] += 1
                return redirect('/instructions/')
            if request.session['instruction'] == 2:
                request.session['instruction'] += 1
                return redirect('/game/')
            else:
                request.session['score'] = request.session['params']['budget']
                request.session['Previous Classification'] = ''
                request.session['block'] += 1
                return redirect('/game/')
        if request.POST['Continue'] == 'Back':
            request.session['instruction'] -= 1
            return redirect('/instructions/')
    if request.method == "GET":
        return render(request=request,
                      template_name=f'Instruction.html',
                      context={'page': request.session['instruction'],
                               'v_tp': int(request.session['params']['v_tp']),
                               'v_fp': int(request.session['params']['v_fp']),
                               'v_tn': int(request.session['params']['v_tn']),
                               'v_fn': int(request.session['params']['v_fn']),
                               'budget': request.session['params']['budget'],
                               'block': request.session['block'], 'order': request.session['order'],
                               'condition': request.session['output'], 'sensitivity': request.session['sensitivity'],
                               'system_cost': request.session['params']['system_cost']})


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def game(request):
    # if not request.user.is_authenticated:
    #     return redirect('/end/')
    if request.session['trial'] > request.session['params']['N']:
        if request.session['block'] > request.session['params']['B']:
            return redirect('/nasa_tlx/')
        else:
            return redirect('/instructions/')
    blue_or_orange = request.session['events'][f"({request.session['block']},{request.session['trial']})"]['type']
    stimulus_h = request.session['events'][f"({request.session['block']},{request.session['trial']})"]['stimulus_h']
    p_h = request.session['events'][f"({request.session['block']},{request.session['trial']})"]['P(Human)']

    if request.session['sensitivity'] == 'low':
        stimulus_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
            'stimulus_s_low']
        output = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
            'P(Low_System_Binary)']
        if request.session['output'] == 'likelihood':
            p_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
                'P(Low_System_Likelihood)']
        else:
            p_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
                'P(Low_System_Integrated)']
    else:
        stimulus_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
            'stimulus_s_high']
        output = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
            'P(High_System_Binary)']
        if request.session['output'] == 'likelihood':
            p_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
                'P(High_System_Likelihood)']
        else:
            p_s = request.session['events'][f"({request.session['block']},{request.session['trial']})"][
                'P(High_System_Integrated)']

    p_id = request.session['id']
    participant_object = Participant.objects.filter(id=p_id).first()
    if request.method == "POST":
        if request.POST['button'] == 'VBN-BLUE':
            user_action = 'Blue'
            if blue_or_orange == 'Blue':
                request.session['Previous Classification'] = 'Correct,you classified it as Blue and it was Blue'
            elif blue_or_orange == 'Orange':
                request.session['Previous Classification'] = 'Wrong, you classified it as Blue but it was Orange'
        elif request.POST['button'] == 'VBN-ORANGE':
            user_action = 'Orange'
            if blue_or_orange == 'Orange':
                request.session['Previous Classification'] = 'Correct, you classified it as Orange and it was Orange'
            elif blue_or_orange == 'Blue':
                request.session['Previous Classification'] = 'Wrong, you classified it as Orange but it was Blue'
        elif request.POST['button'] == 'Use the support system':
            request.session['Information Button'] = False
            request.session['PD'] = True
            request.session['score'] -= request.session['params']['system_cost']
            return redirect('/game/')
        elif request.POST['dummpy_button'] in ['Blue Vibranium', 'Oramge Vibranium']:
            return redirect('/game/')
        try:
            if user_action == blue_or_orange: # The costs equal --> we don't need to differentiate between  P,N
                request.session['score'] += request.session['params']['v_tp']
            else:
                request.session['score'] += request.session['params']['v_fp']
            e = Events.objects.create(id_block_trial=f"{p_id}-{request.session['block']}-{request.session['trial']}",
                                      user_id=participant_object.id,
                                      participant=participant_object, block=request.session['block'],
                                      trial=request.session['trial'],
                                      stimulus_h=stimulus_h, stimulus_s=stimulus_s, p_h=p_h, p_s=p_s, output=output,
                                      pd=not request.session['Information Button'],
                                      event=blue_or_orange,
                                      classification=user_action,
                                      score=round(request.session['score'], 1))
            time.sleep(1)
        except:
            return redirect('/warning/')
        request.session['Information Button'] = True
        e.save()
        if request.session['trial'] == request.session['params']['N']:
            if request.session['block'] == request.session['params']['B']:
                return redirect('/nasa_tlx/')
            else:
                return redirect('/instructions/')

        request.session['trial'] += 1
        return redirect('/game/')
    if request.method == "GET":
        request.session['PD'] = False
        if request.session['Previous Classification'] == '':
            previous_classification_bool = ''
        elif request.session['Previous Classification'][0] == 'W':
            previous_classification_bool = 'Wrong'
        else:
            previous_classification_bool = 'Correct'
        if str(round(request.session['score'], 1))[-1] == '0':
            display_score = int(request.session['score'])
        else:
            display_score = round(request.session['score'], 1)
        return render(request=request,
                      template_name=f'Game.html',
                      context={'p_h': p_h, 'p_s': p_s, 'trial': request.session['trial'],
                               'event_color': blue_or_orange,
                               'total_number': request.session['params']['N'],
                               'additional_information': request.session['Information Button'],
                               'output': output, 'condition': request.session['output'],
                               'block': request.session['block'],
                               'score': display_score,
                               'previous_classification': request.session['Previous Classification'],
                               'previous_classification_bool': previous_classification_bool,
                               'order': request.session['order']})


def server(request):
    if request.method == "POST":
        user_name = request.POST['user name']
        password = request.POST['password']
        if user_name == 'Administrator' and password == '0571JyY':
            if request.POST['setting'] == 'DB':
                save_db()
                return render(request=request, template_name='Successful.html')
            elif request.POST['setting'] == 'Progress':
                return redirect('/progress/')
            elif request.POST['setting'] == 'Parameters':
                return redirect('/parameters/')
            elif request.POST['setting'] == 'Other':
                return render(request=request,
                              template_name='Server.html',
                              context={'flag': 1})
            elif request.POST['setting'] == 'ok':
                Participant.objects.all().delete()
                Events.objects.all().delete()
                Nasa.objects.all().delete()
                Trust.objects.all().delete()

    return render(request=request,
                  template_name='Server.html',
                  context={'flag': 0})


def parameters(request):
    if request.method == "POST":
        user_name = request.POST['user name']
        password = request.POST['password']
        if user_name == 'Administrator' and password == '0571JyY':
            if request.POST['Set parameters'] == 'Set parameters':
                blocks = request.POST['number of blocks']
                events = request.POST['number of events']
                test_events = request.POST['number of test events']
                v_tp = request.POST['v_tp']
                v_fp = request.POST['v_fp']
                v_fn = request.POST['v_fn']
                v_tn = request.POST['v_tn']
                parameters_dict = {'blocks': blocks, 'events': events, 'test_events': test_events,
                                   'v_tp': v_tp, 'v_fp': v_fp, 'v_fn': v_fn, 'v_tn': v_tn}
                save_parameters = pd.DataFrame.from_dict(parameters_dict, orient='index')
                save_parameters.to_csv('parameters/parameters.csv', index=True)
                return render(request=request, template_name='Successful.html')
    return render(request=request,
                  template_name='Parameters.html')


def save_db():
    users_dict = {}
    events_dict = {}

    index = 0
    for user in Participant.objects.all():
        users_dict[index] = [user.id, user.aid, user.condition, user.order,
                             user.start_time, user.end_time, user.total_time,
                             user.user_agent, user.is_pc, user.is_mobile, user.is_tablet, user.is_bot, user.ip,
                             user.finish]
        index += 1
    users_df = pd.DataFrame.from_dict(users_dict, orient='index', columns=['id', 'aid', 'condition', 'order',
                                                                           'start_time', 'end_time', 'total_time',
                                                                           'user_agent', 'is_pc', 'is_mobile', 'is_tablet',
                                                                           'is_bot', 'ip', 'finish'])
    users_df.to_csv('data/users.csv', index=False)

    index = 0
    for event in Events.objects.all():
        events_dict[index] = [event.participant.id, event.participant.aid, event.participant.condition,
                              event.block, event.trial,
                              event.event, event.stimulus_h, event.stimulus_s,
                              event.pd, event.classification, event.time, event.score,
                              event.p_h, event.p_s, event.output]
        index += 1

    event_df = pd.DataFrame.from_dict(events_dict, orient='index', columns=['id', 'aid', 'condition', 'block', 'trial',
                                                                            'event', 'stimulus_h', 'stimulus_s',
                                                                            'pd', 'classification', 'time',
                                                                            'score', 'human_p', 'system_p',
                                                                            'system_output'])
    event_df.to_csv('data/events.csv', index=False)

    nasa_dict = {}
    index = 0
    for nasa in Nasa.objects.all():
        nasa_dict[index] = [nasa.participant.id, nasa.participant.aid, nasa.participant.condition,
                            nasa.system, nasa.mental_demand, nasa.physical_demand, nasa.performance,
                            nasa.effort, nasa.frustration]
        index += 1
    nasa_df = pd.DataFrame.from_dict(nasa_dict, orient='index', columns=['id', 'aid', 'condition', 'system',
                                                                         'mental_demand', 'physical_demand',
                                                                         'performance', 'effort', 'frustration'])
    nasa_df.to_csv('data/nasa.csv', index=False)

    turst_dict = {}
    index = 0
    for trust in Trust.objects.all():
        turst_dict[index] = [trust.participant.id, trust.participant.aid, trust.participant.condition,
                            trust.trust_1, trust.trust_2]
        index += 1
    trust_df = pd.DataFrame.from_dict(turst_dict, orient='index', columns=['id', 'aid', 'condition',
                                                                           'How much the additional information help you in the task?',
                                                                           'How good the additional information in distinguishing between blue and orange events?'])
    trust_df.to_csv('data/trust.csv', index=False)


def progress(request):
    count = Participant.objects.count()
    completed_users = Participant.objects.exclude(finish=False).count()
    condition_1 = Participant.objects.exclude(finish=False).filter(condition=1).count()
    condition_2 = Participant.objects.exclude(finish=False).filter(condition=2).count()
    time = np.array(Participant.objects.filter(finish=True).values_list('total_time', flat=True))
    return render(request=request,
                  template_name='Progress.html',
                  context={'users': count, 'completed_users': completed_users,
                           'condition_1': condition_1, 'condition_2': condition_2,
                           'mean_time': round(time.mean(), 2), 'std_time': round(time.std(), 2)})

def completed(request):
    count = Trust.objects.count()
    return render(request=request,
                  template_name='completed.html',
                  context={'users': count})


def nasa_tlx(request):
    participant_object = Participant.objects.filter(id=request.session['id']).first()
    if request.method == "POST":
        if request.POST['button'] == 'submit':
            mental_demand = request.POST.get('mental_demand')
            physical_demand = request.POST.get('physical_demand')
            performance = request.POST.get('Performance')
            effort = request.POST.get('Effort')
            frustration = request.POST.get('Frustration')
            Nasa.objects.create(participant=participant_object, user_id=participant_object.id,
                                system=request.session['nasa_tlx_system'],
                                mental_demand=mental_demand, physical_demand=physical_demand,
                                performance=performance, effort=effort, frustration=frustration)
            if request.session['nasa_tlx_system']:
                return redirect('/trust/')
            request.session['nasa_tlx_system'] = True

    return render(request=request,
                  template_name='nasa_tlx.html', context={'system': request.session['nasa_tlx_system']})


def trust(request):
    participant_object = Participant.objects.filter(id=request.session['id']).first()
    if request.method == "POST":
        if request.POST['button'] == 'submit':
            trust_1 = request.POST.get('trust_1')
            trust_2 = request.POST.get('trust_2')
            Trust.objects.create(participant=participant_object, user_id=participant_object.id,
                                 trust_1=trust_1, trust_2=trust_2)
            return redirect('/end/')

    return render(request=request, template_name='trust.html')


def warning(request):
    if request.method == "POST":
        request.session['warning'] += 1
        if request.session['warning'] > 2:
            return redirect('/end/')
        if request.POST['Continue'] == 'Continue':
            request.session['trial'] = 1
            request.session['score'] = request.session['params']['budget']
            return redirect('/game/')
        elif request.POST['Continue'] == 'End the experiment':
            return redirect('/end/')
        else:
            return redirect('/warning/')
    if request.method == "GET":
        return render(request=request,
                      template_name='warning.html')
