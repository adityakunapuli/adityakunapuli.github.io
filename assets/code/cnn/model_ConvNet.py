import torch.nn as nn
import torch.nn.functional as F


class ConvNet(nn.Module):
	def __init__(self, init_weights = False):
		super(ConvNet, self).__init__()

		self.conv1 = nn.Conv2d(3, WEIGHTS, 3)
		self.bnorm1 = nn.BatchNorm2d(WEIGHTS)
		self.conv2 = nn.Conv2d(WEIGHTS, WEIGHTS, 3)
		self.bnorm2 = nn.BatchNorm2d(WEIGHTS)
		self.drop_out1 = nn.Dropout(p = 0.2)

		self.conv3 = nn.Conv2d(WEIGHTS, WEIGHTS * 2, 3)
		self.bnorm3 = nn.BatchNorm2d(WEIGHTS * 2)
		self.conv4 = nn.Conv2d(WEIGHTS * 2, WEIGHTS * 2, 3)
		self.bnorm4 = nn.BatchNorm2d(WEIGHTS * 2)
		self.drop_out2 = nn.Dropout(p = 0.3)

		self.conv5 = nn.Conv2d(WEIGHTS * 2, WEIGHTS * 4, 3)
		self.bnorm5 = nn.BatchNorm2d(WEIGHTS * 4)
		self.conv6 = nn.Conv2d(WEIGHTS * 4, WEIGHTS * 4, 3)
		self.bnorm6 = nn.BatchNorm2d(WEIGHTS * 4)
		self.drop_out3 = nn.Dropout(p = 0.4)

		self.fc1 = nn.Linear((WEIGHTS * 4) * 4 * 4, 10)
		self.pool = nn.MaxPool2d(2, 2)  # 2x2 window with stride = 2
		self.softmax = nn.Softmax()

		if init_weights:
			self._initialize_weights()

	def forward(self, x):
		# Pad following pooling in order to maintaing 32x32 size
		pad1 = [1, 1, 1, 1]  # use below padding for alternate kernel sizes in subsequent layers--e.g. 3-4

		x = F.pad(self.bnorm1((F.relu(self.conv1(x)))), pad1, 'constant', 0)
		x = F.pad(self.bnorm2(F.relu(self.conv2(x))), pad1, 'constant', 0)
		x = self.drop_out1(self.pool(x))

		x = F.pad(self.bnorm3((F.relu(self.conv3(x)))), pad1, 'constant', 0)
		x = F.pad(self.bnorm4(F.relu(self.conv4(x))), pad1, 'constant', 0)
		x = self.drop_out2(self.pool(x))

		x = F.pad(self.bnorm5((F.relu(self.conv5(x)))), pad1, 'constant', 0)
		x = F.pad(self.bnorm6(F.relu(self.conv6(x))), pad1, 'constant', 0)
		x = self.drop_out3(self.pool(x))

		x = x.view(-1, (WEIGHTS * 4) * 4 * 4)
		x = self.fc1(x)
#		x = self.softmax(x)
		return x

	def _initialize_weights(self):
		for m in self.modules():
			if isinstance(m, nn.Conv2d):
				nn.init.kaiming_normal_(m.weight, mode = 'fan_out', nonlinearity = 'relu')
				if m.bias is not None:
					nn.init.constant_(m.bias, 0)
			elif isinstance(m, nn.BatchNorm2d):
				nn.init.constant_(m.weight, 1)
				nn.init.constant_(m.bias, 0)
			elif isinstance(m, nn.Linear):
				nn.init.normal_(m.weight, 0, 0.01)
				nn.init.constant_(m.bias, 0)
