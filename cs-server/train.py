import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import MNIST
from torchvision import transforms
import torch
import torch.nn.functional as F
import torch.nn as nn
from pytorch_lightning.callbacks import ModelCheckpoint
import os

# default values, 1 node, 1 gpu
NGPUS = int(os.getenv("NUM_GPUS", 1))       # Number of GPUs per node
NNODES = int(os.getenv("NUM_NODES", 1))

# Define a simple CNN model
class LitMNISTModel(pl.LightningModule):
    def __init__(self):
        super(LitMNISTModel, self).__init__()
        self.layer1 = nn.Conv2d(1, 32, 3, 1)
        self.layer2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        self.log("val_loss", loss)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

# Load and prepare the MNIST dataset
def prepare_data():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    mnist_train = MNIST('', train=True, download=True, transform=transform)
    mnist_val = MNIST('', train=False, download=True, transform=transform)

    train_loader = DataLoader(mnist_train, batch_size=64, shuffle=True)
    val_loader = DataLoader(mnist_val, batch_size=64)
    return train_loader, val_loader

if __name__ == "__main__":
    # Prepare data
    train_loader, val_loader = prepare_data()

    # Initialize model
    model = LitMNISTModel()

    # Initialize trainer with distributed strategy
    trainer = pl.Trainer(
        accelerator='gpu',        # Use GPU
        strategy='ddp',           # DistributedDataParallel strategy
        devices=NGPUS,                # Number of GPUs per node
        num_nodes=NNODES,              # Number of nodes
        max_epochs=5,             # Train for 5 epochs
        callbacks=[ModelCheckpoint(dirpath='checkpoints/', monitor='val_loss')]
    )

    # Start training
    trainer.fit(model, train_loader, val_loader)
