from method.ICDM.icdm import ICDM
from method.ICDM.icdm_ind import ICDM as ICDMIND
from runners.ICDM.utils import save
import numpy as np


def icdm_runner(config, save):
    icdm = ICDM(stu_num=config['stu_num'], prob_num=config['prob_num'], know_num=config['know_num'],
                 dim=config['dim'], device=config['device'], gcn_layers=config['gcnlayers'],
                 weight_reg=config['weight_reg'],
                 graph=config['graph_dict'], agg_type=config['agg_type'], cdm_type=config['cdm_type'],
                 khop=config['khop'])
    icdm.train(config['np_train'], config['np_test'], q=config['q'], batch_size=config['batch_size'],
                epoch=config['epoch'], lr=config['lr'])
    save(config, icdm.mas_list)


def get_runner(method: str):
    if 'icdm' in method:
        return icdm_runner
    else:
        raise ValueError('This method is currently not supported.')


def icdm_ind_runner(config, save):
    if config['ab'] == 'tf':
        config['dim'] = config['know_num']
    icdm = ICDMIND(stu_num=config['stu_num'], prob_num=config['prob_num'], know_num=config['know_num'],
                     dim=config['dim'], device=config['device'], gcn_layers=config['gcnlayers'],
                     weight_reg=config['weight_reg'],
                     graph=config['graph_dict'], agg_type=config['agg_type'], exist_idx=config['exist_idx'],
                     new_index=config['new_idx'], mode=config['mode'], cdm_type=config['cdm_type'], khop=config['khop'],
                     ab=config['ab'], d_1=config['d_1'], d_2=config['d_2'])
    icdm.train(config['np_train_old'], config['np_train_new'], config['np_test'], config['np_test_new'], q=config['q'],
                batch_size=config['batch_size'],
                epoch=config['epoch'], lr=config['lr'])
    save(config, icdm.mas_list)


def icdm_re_ind_runner(config, save):
    icdm = ICDM(stu_num=config['stu_num'], prob_num=config['prob_num'], know_num=config['know_num'],
                  dim=config['dim'], device=config['device'], gcn_layers=config['gcnlayers'],
                  weight_reg=config['weight_reg'],
                  graph=config['graph_dict'], agg_type=config['agg_type'], exist_idx=config['exist_idx'],
                  new_idx=config['new_idx'], cdm_type=config['cdm_type'], khop=config['khop'])
    icdm.train(np.vstack((config['np_train_old'], config['np_train_new'])), config['np_test'], config['np_test_new'],
                q=config['q'],
                batch_size=config['batch_size'],
                epoch=config['epoch'], lr=config['lr'])
    save(config, icdm.mas_list)


def get_ind_runner(method: str):
    if 'icdm' in method:
        if 'icdm-re' not in method:
            return icdm_ind_runner
        else:
            return icdm_re_ind_runner
    else:
        raise ValueError('This method is currently not supported.')
