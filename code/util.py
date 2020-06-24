import os,time
import numpy as np
import tensorflow as tf

    
def suppress_tf_warning():
    import tensorflow as tf
    import os
    import logging
    from tensorflow.python.util import deprecation
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # tf.logging.set_verbosity(tf.logging.ERROR)
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    logging.getLogger('tensorflow').disabled = True
    deprecation._PRINT_DEPRECATION_WARNINGS = False
    

class ReplayBuffer:
    """
    A simple FIFO experience replay buffer for SAC agents.
    """
    def __init__(self, obs_dim, act_dim, size):
        self.obs1_buf = np.zeros([size, obs_dim], dtype=np.float32)
        self.obs2_buf = np.zeros([size, obs_dim], dtype=np.float32)
        self.acts_buf = np.zeros([size, act_dim], dtype=np.float32)
        self.rews_buf = np.zeros(size, dtype=np.float32)
        self.done_buf = np.zeros(size, dtype=np.float32)
        self.ptr, self.size, self.max_size = 0, 0, size

    def store(self, obs, act, rew, next_obs, done):
        self.obs1_buf[self.ptr] = obs
        self.obs2_buf[self.ptr] = next_obs
        self.acts_buf[self.ptr] = act
        self.rews_buf[self.ptr] = rew
        self.done_buf[self.ptr] = done
        self.ptr = (self.ptr+1) % self.max_size
        self.size = min(self.size+1, self.max_size)

    def sample_batch(self, batch_size=32):
        idxs = np.random.randint(0, self.size, size=batch_size)
        return dict(obs1=self.obs1_buf[idxs],
                    obs2=self.obs2_buf[idxs],
                    acts=self.acts_buf[idxs],
                    rews=self.rews_buf[idxs],
                    done=self.done_buf[idxs])
        
def gpu_sess():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    return sess

t_start_tictoc = time.time()
def tic():
    global t_start_tictoc
    t_start_tictoc = time.time()
    
def toc(toc_str=None):
    global t_start_tictoc
    t_elapsed_sec = time.time() - t_start_tictoc
    if toc_str is None:
        print ("Elapsed time is [%.4f]sec."%
        (t_elapsed_sec))
    else:
        print ("[%s] Elapsed time is [%.4f]sec."%
        (toc_str,t_elapsed_sec))