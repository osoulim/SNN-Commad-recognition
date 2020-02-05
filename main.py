import glob
from random import shuffle

from Model import Model
from wave2spike import wave2spike

filenames = glob.glob("dataset/*")[:200]
shuffle(filenames)
files_num = len(filenames)

train_size = 199
train_files = filenames[0: train_size]
test_files = filenames[train_size:]

anf_size = 26
model = Model([anf_size, 10])
# print(list(map(lambda x: x.delay, model.synapses.values())))

print("learning started")
for file_id, file_name in enumerate(train_files):
    # print('\r learning %d %% completed' % (file_id * 100 // train_size))
    spikes_data = wave2spike(file_name, anf_size)
    for neuron_id, spike_data in enumerate(spikes_data):
        for spike_time in spike_data["spikes"] * 10000:
            model.add_spike_to_input(neuron_id, spike_time)

    while not model.is_queue_empty():
        model.next_step()

    model.reset()

print("learning finished")
model.disable_learning()

for file_name in test_files:
    spikes_data = wave2spike(file_name, anf_size)
    for neuron_id, spike_data in enumerate(spikes_data):
        for spike_time in spike_data["spikes"] * 10000:
            model.add_spike_to_input(neuron_id, spike_time)

    print(file_name, "-------------------------")
    while not model.is_queue_empty():
        model.next_step()
    model.reset()

