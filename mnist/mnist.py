from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

##### BEGIN CUSTOM CLUSTER OVERHEAD
import os
import signal
import sys

class ClusterStateManager:
    def __init__(self, time_to_run=600):
        self.external_exit = None
        self.timer_exit = False

        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGALRM, self.timer_handler)
        signal.alarm(time_to_run)

    def signal_handler(self, signal, frame):
        print("Received signal [", signal, "]")
        self.external_exit = signal

    def timer_handler(self, signal, frame):
        print("Received alarm [", signal, "]")
        self.timer_exit = True

    def should_exit(self):
        if self.timer_exit:
            return True

        if self.external_exit is not None:
            return True

        return False

    def get_exit_code(self):
        if self.timer_exit:
            return 3

        if self.external_exit is not None:
            return 0

        return 0

def save(network, optimizer, epoch):
    full_training_state = {"network": network.state_dict(),
                 "optimizer": optimizer.state_dict(),
                 "epoch": epoch}
    torch.save(full_training_state, "data/mnist_cnn.pt")

def load(network, optimizer):
    if not os.path.exists("data/mnist_cnn.pt"):
        return 0

    checkpoint = torch.load("data/mnist_cnn.pt")
    network.load_state_dict( checkpoint['network'] )
    optimizer.load_state_dict( checkpoint['optimizer'] )

    return checkpoint['epoch']

# Start the timer on how long you're allowed to run
csm = ClusterStateManager(30)

##### END CUSTOM CLUSTER OVERHEAD

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def train(model, device, train_loader, optimizer, epoch, log_interval):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        # Test if you should exit.
        # ClusterStateManager will create signal handlers for and 
        # create a state for you to query
        if csm.should_exit():
            return

        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


def main():
    # Training settings
    batch_size = 64
    epochs = 60
    lr = 2e-4
    gamma = 0.7
    log_interval = 10

    use_cuda = torch.cuda.is_available()

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=batch_size, shuffle=True, **kwargs)

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=lr)

    # Load the model, optimizer, and current epoch
    cur_epoch = load(model, optimizer)

    scheduler = StepLR(optimizer, step_size=1, gamma=gamma)
    for epoch in range(cur_epoch, epochs + 1):
        train(model, device, train_loader, optimizer, epoch, log_interval)
        scheduler.step()

        # Once again check if we should exit
        if csm.should_exit():
            break

    # save the current state that you're in and include the current epoch
    save(model, optimizer, epoch)

    # Exit with the exit code the ClusterStateManager has set for you
    print("Exiting with exit code", csm.get_exit_code())
    sys.exit(csm.get_exit_code())


if __name__ == '__main__':
    main()
