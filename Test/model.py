from extractDataset import *

from keras.utils import np_utils,to_categorical
from keras.optimizers import RMSprop, Adam
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, BatchNormalization, Conv1D, Conv2D, MaxPooling2D, MaxPooling1D
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from keras import optimizers

import tensorflow as tf

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, GridSearchCV
from sklearn import preprocessing
from sklearn.metrics import plot_confusion_matrix

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
MOVES_FOR_WEEK_9 = ['gun', 'sidepump', 'hair']
USE_FEATURES = True

def saveWeightstoFile(fname,weights):
    
    with open(fname, 'w') as f:
        w = list(map(lambda x: x.tolist(), weights))
        print(w, file=f)
        

def convertToQuantized(mod, data):
    converter = tf.lite.TFLiteConverter.from_keras_model(mod)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.representative_dataset = data
    converter.inference_input_type = tf.float32
    converter.inference_output_type = tf.float32
    tflite_quant_model = converter.convert()
    return tflite_quant_model
    
def importAndPrepareData(testset =False):
    Xs = []
    Y_string = []
    Y = []

    data = processData(testset = testset)

    for dm in data:
        if USE_FEATURES:
            dm.extractAllFeatures()
            arr = dm.getFeaturesAsListOfFlattenedArray()
            flatArray = np.array(arr)
            # print(flatArray.shape)
            Xs.extend(arr)
            Y_string.extend([dm.movename]*flatArray.shape[0])
        else:
            arr = dm.getDataAsNumpyArray()
            arr = np.ravel(arr)
            Xs.append(arr)
            Y_string.append(dm.movename)
            if not arr.shape == (600,) or not arr.dtype == "float64":
                print(dm.get_data())
                print(arr.shape, arr.dtype)
                assert False

    print(np.array(Xs).shape)
    encoder = preprocessing.LabelEncoder()
    encoder.fit(Y_string)
    Y = encoder.fit_transform(Y_string)
    print(encoder.classes_)

    # print(Y)
    return (np.array(Xs),np.array(Y), encoder)



def perform_mlp(fold, X , y, enc,  Xs_TEST,Y_TEST):
    noclasses = 8
    k = 1
    # kf = StratifiedKFold(n_splits=k, shuffle=True)

    scores = []

    Y_TEST_Catergorical = to_categorical(Y_TEST, num_classes=noclasses)
    c = 0

    # for i in range(5):
    #     fname = "example_{}_Output_is_{}".format(i,y[i])
    #     with open(fname, 'w') as f:
    #         w = X[i].tolist()
    #         print(w, file=f)
    #         print(X[i].shape, file=f)

    # return 
    # for train_index, test_index in kf.split(X, y):
    for dasdas in [1]:

        
        # X_train , X_test = X[train_index,:], X[test_index,:]
        # y_train , y_test = y[train_index], y[test_index]

        
        
        # print("X_train {} X_test {}".format(X_train.shape , X_test.shape))

        # y_test_without_transform = y_test
        # y_train = to_categorical(y_train, num_classes=noclasses)
        # y_test = to_categorical(y_test, num_classes=noclasses)

        X_train, y_train = X , to_categorical(y, num_classes=noclasses)
        X_test, y_test = Xs_TEST,Y_TEST_Catergorical

        def mlp_model():
            model = Sequential()
            model.add(Dense(units=64, kernel_initializer='uniform', activation='relu', input_shape = X_train[0].shape))
            # model.add(Dropout(0.2))
            model.add(Dense(units=64, kernel_initializer='uniform', activation='relu'))
            model.add(Dense(units=noclasses, kernel_initializer='uniform', activation='softmax'))
            model.compile(optimizer=Adam(learning_rate=0.0001/20), loss='categorical_crossentropy', metrics=['accuracy'])
            return model
        
        mlp = mlp_model()
        # print(mlp.summary())        
        
        checkpoint_filepath="MLP_weights_checkpoint.hdf5"
                
        my_callbacks = [
            EarlyStopping(monitor='val_loss', mode='min', verbose=0, patience=20),
            ReduceLROnPlateau(monitor='val_accuracy', factor=0.1, min_delta=0.00001, patience=20, verbose=0),
            ModelCheckpoint(filepath = checkpoint_filepath, save_weights_only=True, monitor='val_accuracy',
                            verbose=1, save_best_only=True, mode='max')  
        ] 
        
        history = mlp.fit(X_train, y_train, batch_size=512, epochs=750, validation_data=(X_test, y_test), verbose = 1, shuffle=True) #  callbacks=my_callbacks)
        
        
        mlp_pred = np.argmax(mlp.predict(X_test), axis=-1)
        twin = []
        twin.append(mlp.evaluate(X_test, y_test, batch_size=64, verbose=1))
        twin.append(mlp.evaluate(Xs_TEST, Y_TEST_Catergorical, batch_size=64, verbose=1))

        mlp.save('fold_{}_acc_{}'.format(c,twin[1][1]))
        scores.append(twin)

        
        # mlp_weights = mlp.get_weights()
        # print("MLP Weights:", mlp_weights)
        
        # mlp.save('saved_models/MLP_99.6_accuracy')
        
        # print('y_test\n', y_test_without_transform)
        print('')
        print('mlp_pred\n', mlp_pred)
        weights = mlp.get_weights()
        fname = "weights{}".format(c)
        c+=1
        # saveWeightstoFile(fname,weights)
        mlp_pred = np.argmax(mlp.predict(Xs_TEST), axis=-1)
        cm  = confusion_matrix(Y_TEST, mlp_pred)
        a = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=enc.classes_)
        a.plot()
    for idx, s in enumerate(scores):
        print("Fold: {} ".format(idx))
        for twin in s:
            for i,n in enumerate(mlp.metrics_names):
                print("{} : {}".format(n, twin[i]))
        print('')
    print("X_train {} X_test {}".format(X_train.shape , X_test.shape))    
    plt.show()
    plt.clf()

import pickle
LOAD_CACHE= True
SAVE_CACHE = True
if __name__ == "__main__":
    if LOAD_CACHE:
        Xs, Y , enc,Xs_TEST, Y_TEST, enc = pickle.load( open( "cache.p", "rb" ) )
    else:
        Xs, Y , enc = importAndPrepareData()
        Xs_TEST, Y_TEST, enc = importAndPrepareData(testset=True)

        if SAVE_CACHE:
            pickle.dump( [Xs, Y , enc,Xs_TEST, Y_TEST, enc], open( "cache.p", "wb" ) )

    # sys.exit(1)
    perform_mlp(5, Xs , Y , enc, Xs_TEST,Y_TEST )

    