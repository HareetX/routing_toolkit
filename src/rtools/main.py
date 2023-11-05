from argparse import ArgumentParser
from numpy import mean

from rtools.dataset import Dataset
from rtools.modeling.grid_env import GridEnv
from rtools.router import AStarRouter

from rtools.visualizer import MiniMap


def routing_arguments():
    parser = ArgumentParser('AStarSolver')
    parser.add_argument('--episode', type=int, dest='episode', default=1)
    parser.add_argument('--log', type=str, dest='log', default="log.txt")  # TODO
    parser.add_argument('--trace', type=bool, dest='trace', default=True)  # TODO
    parser.add_argument('--kicad_dir', type=str, dest='kicad_dir', default="example/pcb/bench2/")
    parser.add_argument('--kicad_pcb', type=str, dest='kicad_pcb', default="bm2.unrouted.kicad_pcb")
    parser.add_argument('--kicad_pro', type=str, dest='kicad_pro', default="bm2.unrouted.kicad_pro")
    parser.add_argument('--save_file', type=str, dest='save_file', default="bm2.routed.kicad_pcb")

    return parser.parse_args()


if __name__ == '__main__':
    # get the routing arguments
    arg = routing_arguments()

    # get the file name
    pcb_dir = arg.kicad_dir
    pcb_file = pcb_dir + arg.kicad_pcb
    pro_file = pcb_dir + arg.kicad_pro
    save_file = arg.save_file

    # build the dateset from the file
    dataset = Dataset(pcb_dir, pcb_file, pro_file, save_file)
    # load the routing data
    dataset.load()

    # tmp = dataset.netList[1]
    # dataset.netList[1] = dataset.netList[14]
    # dataset.netList[14] = tmp

    # tmp = dataset.netList[2]
    # dataset.netList[2] = dataset.netList[15]
    # dataset.netList[15] = tmp

    # build the model from dataset

    area = [[dataset.board_area[1], dataset.board_area[3], 0], [dataset.board_area[0], dataset.board_area[2], 1]]

    # area = [[0, 0, 0], [0, 0, -1]]

    # bm1 PL0-7 bus routing area
    # start_area = [[146.56, 110.24, 0], [150.90, 112.27, 0]]
    # cell1_area = [[141.90, 112.27, 0], [157.66, 122.09, 0]]
    # cell2_area = [[157.66, 114.30, 0], [182.17, 122.09, 0]]
    # cell3_area = [[182.17, 107.51, 0], [190.16, 122.09, 0]]
    # end_area = [[190.16, 107.51, 0], [195.58, 118.08, 0]]

    # bm1 PA3-7 bus routing area
    # start_area = [[155.55, 94.30, 0], [157.47, 99.79, 0]]
    # cell1_area = [[157.47, 82.50, 0], [160.27, 100.15, 0]]
    # cell2_area = [[160.27, 82.5, 0], [190.03, 93.37, 0]]
    # cell3_area = [[185.65, 91.08, 0], [190.03, 98.12, 0]]
    # end_area = [[190.03, 81.73, 0], [195.31, 92.88, 0]]

    # bm1 PA0-2 bus routing area
    # start_area = [[153.04, 94.27, 0], [154.94, 96.30, 0]]
    # cell1_area = [[142.07, 82.58, 0], [157.38, 94.27, 0]]
    # cell2_area = [[157.38, 82.58, 0], [189.94, 90.27, 0]]
    # end_area = [[189.94, 81.76, 0], [195.72, 87.81, 0]]

    # bm1 PC0-7 bus routing area
    # start_area = [[155.38, 104.31, 0], [157.62, 108.58, 0]]
    # cell1_area = [[157.62, 100.04, 0], [176.92, 111.76, 0]]
    # cell2_area = [[176.92, 98.02, 0], [179.86, 111.76, 0]]
    # cell3_area = [[179.86, 91.31, 0], [190.09, 111.76, 0]]
    # end_area = [[190.09, 91.99, 0], [195.37, 103.19, 0]]

    # bm1 ADC0-15 bus routing area
    # start_area = [[143.17, 94.41, 0], [151.83, 96.21, 0]]
    # cell1_area = [[142.10, 82.70, 0], [156.96, 94.41, 1]]
    # cell2_area = [[142.10, 94.41, 1], [156.96, 114.21, 1]]
    # cell3_area = [[142.10, 114.21, 1], [190.19, 127.40, 1]]
    # end_area = [[147.08, 127.40, 1], [190.52, 130.85, 1]]

    model = GridEnv(dataset.board_area, dataset.layers_, dataset.netNum, dataset.net_order,
                    dataset.netList, dataset.netClass, dataset.pad_obstacles,
                    [area])

    # demo = MiniMap(model, 3, 0.05)

    # build the router based on the model
    router = AStarRouter(model)
    # routing...
    router.run(arg.episode)

    # demo = MiniMap(model, 3, 0.05)

    # write back the routing result
    route_combo = model.merge_route()
    # tmp = route_combo[0]
    # route_combo[0] = route_combo[13]
    # route_combo[13] = tmp

    # tmp = route_combo[1]
    # route_combo[1] = route_combo[14]
    # route_combo[14] = tmp
    dataset.store_route(route_combo)

    dataset.save()

    print('\nroute time = {} s'.format(router.route_time))
    # print('expend time (ns) : {}'.format(router.expend_time))
    print('avg expend time : {} ns'.format(mean(router.expend_time)))
    print('sum expend time : {} s'.format(router.sum_expend_time / 1000000000))
    print('get neighbors time : {} s'.format(router.get_neighbors_time / 1000000000))
    print('calculate space cost time : {} s'.format(router.calculate_space_cost_time / 1000000000))
    print('add neighbors time : {} s'.format(router.add_neighbors_time / 1000000000))
    print('routing cost : {}'.format(router.route_cost))
    print('episode cost : {}'.format(router.episode_cost))
