import yaml
import json
import argparse
#from calculate_trainset_mean_std import cal_dir_stat_parallel

def data_preprocessing(args):
    with open(args.coco_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        coco = yaml.load(file, Loader=yaml.FullLoader)

    import json
    with open(args.train_path) as file:
        temp = json.load(file)

    categories = []
    for category_data in temp['categories']:
        categories.append(category_data['name'])

    # rgb_mean, rgb_std = cal_dir_stat_parallel(args.train_data_path)

    coco['obj_list'] = list(categories)
    coco['project_name'] = args.project_name
    coco['train_set'] = 'train'
    coco['val_set'] = 'val'
    coco['num_gpus'] = args.num_gpus

    # coco['mean'] = rgb_mean
    # coco['std'] = rgb_std

    coco['mean'] = list([0.485, 0.456, 0.406])
    coco['std'] = list([0.229, 0.224, 0.225])

    with open(args.output_path, 'w') as file:
        documents = yaml.safe_dump(coco, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create project YAML file')
    parser.add_argument('--coco_path', dest='coco_path', type=str,
                     help='Path to COCO YAML file')
    parser.add_argument('--train_path', dest='train_path', type=str,
                     help='Path to coco train json file')
    parser.add_argument('--train_data_path', dest='train_data_path', type=str,
                     help='Path to training dataset')
    parser.add_argument('--project_name', dest='project_name', type=str,
                     help='Project Name')
    parser.add_argument('--output_path', dest='output_path', type=str,
                     help='Path to output project YAML file')
    parser.add_argument('--num_gpus', dest='num_gpus', type=str,
                     help='Number of GPUs')
    args = parser.parse_args()
    args.num_gpus = int(args.num_gpus)
    data_preprocessing(args)
