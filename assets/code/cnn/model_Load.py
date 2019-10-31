from torchvision.datasets import CIFAR10 as CIFAR10
from torchvision.datasets import ImageFolder as ImageFolder
from torch.utils.data import DataLoader as DataLoader
import torchvision.transforms as Transforms


class LoadModel:
	# def __init__(self, model, dataset_name):
	# 	self.model = model
	# 	self.dataset_name = dataset_name
	def transform_type(self, model):
		model = model.lower()
		if 'conv' in model or 'google' in model:
			print('conv/google')
			normalize = Transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
			transform_train = Transforms.Compose([Transforms.RandomCrop(32, padding = 4),
												Transforms.RandomHorizontalFlip(),
												Transforms.Resize(32),
												Transforms.ToTensor(),
												normalize])
			transform_test = Transforms.Compose([Transforms.Resize(32),
												Transforms.ToTensor(),
												normalize])
		else:
			print('general')
			normalize = Transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
			transform_train = Transforms.Compose([Transforms.RandomResizedCrop(224),
												Transforms.RandomHorizontalFlip(),
												Transforms.ToTensor(),
												normalize])
			transform_test = Transforms.Compose([Transforms.Resize(256),
												Transforms.CenterCrop(224),
												Transforms.ToTensor(),
												normalize])
		return transform_train, transform_test

	def load_data(self, dataset_name, transform_train, transform_test, batchsize = 4, numworkers = 2):
		dataset_name = dataset_name.lower()
		data_path = '/content/drive/My Drive/datasets/'
		if 'cifar' in dataset_name:
			print('Dataset: CIFAR10')
			data_path = data_path + 'CIFAR10/'
			train_set = CIFAR10(root = data_path, train = True, download = False, transform = transform_train)
			test_set = CIFAR10(root = data_path, train = False, download = False, transform = transform_test)
			classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
			num_images, num_train, num_test = [60000, 50000, 10000]
		elif 'bmw' in dataset_name:
			print('Dataset: BMW')
			data_path = data_path + 'bmw10/'
			train_set = ImageFolder(data_path + 'train/', transform = transform_train)
			test_set = ImageFolder(data_path + 'test/', transform = transform_test)
			classes = (1, 2, 3, 4, 5, 6, 7, 8, 10, 11)
		else:
			print('Error: choose a dataset')
		train_loader = DataLoader(train_set, batch_size = batchsize, shuffle = True, num_workers = numworkers)
		test_loader = DataLoader(test_set, batch_size = batchsize, shuffle = False, num_workers = numworkers)
		print('Classes: ' + str(classes)[1:-1])
		return train_loader, test_loader, classes
