??
??
B
AssignVariableOp
resource
value"dtype"
dtypetype?
~
BiasAdd

value"T	
bias"T
output"T" 
Ttype:
2	"-
data_formatstringNHWC:
NHWCNCHW
8
Const
output"dtype"
valuetensor"
dtypetype
.
Identity

input"T
output"T"	
Ttype
q
MatMul
a"T
b"T
product"T"
transpose_abool( "
transpose_bbool( "
Ttype:

2	
e
MergeV2Checkpoints
checkpoint_prefixes
destination_prefix"
delete_old_dirsbool(?

NoOp
M
Pack
values"T*N
output"T"
Nint(0"	
Ttype"
axisint 
C
Placeholder
output"dtype"
dtypetype"
shapeshape:
@
ReadVariableOp
resource
value"dtype"
dtypetype?
E
Relu
features"T
activations"T"
Ttype:
2	
[
Reshape
tensor"T
shape"Tshape
output"T"	
Ttype"
Tshapetype0:
2	
o
	RestoreV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0?
l
SaveV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0?
?
Select
	condition

t"T
e"T
output"T"	
Ttype
H
ShardedFilename
basename	
shard

num_shards
filename
9
Softmax
logits"T
softmax"T"
Ttype:
2
?
StatefulPartitionedCall
args2Tin
output2Tout"
Tin
list(type)("
Tout
list(type)("	
ffunc"
configstring "
config_protostring "
executor_typestring ?
@
StaticRegexFullMatch	
input

output
"
patternstring
N

StringJoin
inputs*N

output"
Nint(0"
	separatorstring 
?
VarHandleOp
resource"
	containerstring "
shared_namestring "
dtypetype"
shapeshape"#
allowed_deviceslist(string)
 ?"serve*2.4.12v2.4.0-49-g85c8b2a817f8ܰ
}
dense_348/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape:	?@*!
shared_namedense_348/kernel
v
$dense_348/kernel/Read/ReadVariableOpReadVariableOpdense_348/kernel*
_output_shapes
:	?@*
dtype0
t
dense_348/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:@*
shared_namedense_348/bias
m
"dense_348/bias/Read/ReadVariableOpReadVariableOpdense_348/bias*
_output_shapes
:@*
dtype0
|
dense_349/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:@*!
shared_namedense_349/kernel
u
$dense_349/kernel/Read/ReadVariableOpReadVariableOpdense_349/kernel*
_output_shapes

:@*
dtype0
t
dense_349/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:*
shared_namedense_349/bias
m
"dense_349/bias/Read/ReadVariableOpReadVariableOpdense_349/bias*
_output_shapes
:*
dtype0
|
dense_350/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:*!
shared_namedense_350/kernel
u
$dense_350/kernel/Read/ReadVariableOpReadVariableOpdense_350/kernel*
_output_shapes

:*
dtype0
t
dense_350/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:*
shared_namedense_350/bias
m
"dense_350/bias/Read/ReadVariableOpReadVariableOpdense_350/bias*
_output_shapes
:*
dtype0
f
	Adam/iterVarHandleOp*
_output_shapes
: *
dtype0	*
shape: *
shared_name	Adam/iter
_
Adam/iter/Read/ReadVariableOpReadVariableOp	Adam/iter*
_output_shapes
: *
dtype0	
j
Adam/beta_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_nameAdam/beta_1
c
Adam/beta_1/Read/ReadVariableOpReadVariableOpAdam/beta_1*
_output_shapes
: *
dtype0
j
Adam/beta_2VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_nameAdam/beta_2
c
Adam/beta_2/Read/ReadVariableOpReadVariableOpAdam/beta_2*
_output_shapes
: *
dtype0
h

Adam/decayVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name
Adam/decay
a
Adam/decay/Read/ReadVariableOpReadVariableOp
Adam/decay*
_output_shapes
: *
dtype0
x
Adam/learning_rateVarHandleOp*
_output_shapes
: *
dtype0*
shape: *#
shared_nameAdam/learning_rate
q
&Adam/learning_rate/Read/ReadVariableOpReadVariableOpAdam/learning_rate*
_output_shapes
: *
dtype0
^
totalVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_nametotal
W
total/Read/ReadVariableOpReadVariableOptotal*
_output_shapes
: *
dtype0
^
countVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_namecount
W
count/Read/ReadVariableOpReadVariableOpcount*
_output_shapes
: *
dtype0
b
total_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name	total_1
[
total_1/Read/ReadVariableOpReadVariableOptotal_1*
_output_shapes
: *
dtype0
b
count_1VarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name	count_1
[
count_1/Read/ReadVariableOpReadVariableOpcount_1*
_output_shapes
: *
dtype0
?
Adam/dense_348/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:	?@*(
shared_nameAdam/dense_348/kernel/m
?
+Adam/dense_348/kernel/m/Read/ReadVariableOpReadVariableOpAdam/dense_348/kernel/m*
_output_shapes
:	?@*
dtype0
?
Adam/dense_348/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:@*&
shared_nameAdam/dense_348/bias/m
{
)Adam/dense_348/bias/m/Read/ReadVariableOpReadVariableOpAdam/dense_348/bias/m*
_output_shapes
:@*
dtype0
?
Adam/dense_349/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape
:@*(
shared_nameAdam/dense_349/kernel/m
?
+Adam/dense_349/kernel/m/Read/ReadVariableOpReadVariableOpAdam/dense_349/kernel/m*
_output_shapes

:@*
dtype0
?
Adam/dense_349/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:*&
shared_nameAdam/dense_349/bias/m
{
)Adam/dense_349/bias/m/Read/ReadVariableOpReadVariableOpAdam/dense_349/bias/m*
_output_shapes
:*
dtype0
?
Adam/dense_350/kernel/mVarHandleOp*
_output_shapes
: *
dtype0*
shape
:*(
shared_nameAdam/dense_350/kernel/m
?
+Adam/dense_350/kernel/m/Read/ReadVariableOpReadVariableOpAdam/dense_350/kernel/m*
_output_shapes

:*
dtype0
?
Adam/dense_350/bias/mVarHandleOp*
_output_shapes
: *
dtype0*
shape:*&
shared_nameAdam/dense_350/bias/m
{
)Adam/dense_350/bias/m/Read/ReadVariableOpReadVariableOpAdam/dense_350/bias/m*
_output_shapes
:*
dtype0
?
Adam/dense_348/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:	?@*(
shared_nameAdam/dense_348/kernel/v
?
+Adam/dense_348/kernel/v/Read/ReadVariableOpReadVariableOpAdam/dense_348/kernel/v*
_output_shapes
:	?@*
dtype0
?
Adam/dense_348/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:@*&
shared_nameAdam/dense_348/bias/v
{
)Adam/dense_348/bias/v/Read/ReadVariableOpReadVariableOpAdam/dense_348/bias/v*
_output_shapes
:@*
dtype0
?
Adam/dense_349/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape
:@*(
shared_nameAdam/dense_349/kernel/v
?
+Adam/dense_349/kernel/v/Read/ReadVariableOpReadVariableOpAdam/dense_349/kernel/v*
_output_shapes

:@*
dtype0
?
Adam/dense_349/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:*&
shared_nameAdam/dense_349/bias/v
{
)Adam/dense_349/bias/v/Read/ReadVariableOpReadVariableOpAdam/dense_349/bias/v*
_output_shapes
:*
dtype0
?
Adam/dense_350/kernel/vVarHandleOp*
_output_shapes
: *
dtype0*
shape
:*(
shared_nameAdam/dense_350/kernel/v
?
+Adam/dense_350/kernel/v/Read/ReadVariableOpReadVariableOpAdam/dense_350/kernel/v*
_output_shapes

:*
dtype0
?
Adam/dense_350/bias/vVarHandleOp*
_output_shapes
: *
dtype0*
shape:*&
shared_nameAdam/dense_350/bias/v
{
)Adam/dense_350/bias/v/Read/ReadVariableOpReadVariableOpAdam/dense_350/bias/v*
_output_shapes
:*
dtype0

NoOpNoOp
?)
ConstConst"/device:CPU:0*
_output_shapes
: *
dtype0*?)
value?)B?) B?)
?
layer-0
layer_with_weights-0
layer-1
layer-2
layer_with_weights-1
layer-3
layer_with_weights-2
layer-4
	optimizer
regularization_losses
	variables
	trainable_variables

	keras_api

signatures
R
regularization_losses
	variables
trainable_variables
	keras_api
h

kernel
bias
regularization_losses
	variables
trainable_variables
	keras_api
R
regularization_losses
	variables
trainable_variables
	keras_api
h

kernel
bias
regularization_losses
	variables
trainable_variables
	keras_api
h

 kernel
!bias
"regularization_losses
#	variables
$trainable_variables
%	keras_api
?
&iter

'beta_1

(beta_2
	)decay
*learning_ratemTmUmVmW mX!mYvZv[v\v] v^!v_
 
*
0
1
2
3
 4
!5
*
0
1
2
3
 4
!5
?
regularization_losses
	variables

+layers
,non_trainable_variables
	trainable_variables
-layer_metrics
.layer_regularization_losses
/metrics
 
 
 
 
?
regularization_losses
	variables

0layers
1non_trainable_variables
trainable_variables
2layer_metrics
3layer_regularization_losses
4metrics
\Z
VARIABLE_VALUEdense_348/kernel6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUE
XV
VARIABLE_VALUEdense_348/bias4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUE
 

0
1

0
1
?
regularization_losses
	variables

5layers
6non_trainable_variables
trainable_variables
7layer_metrics
8layer_regularization_losses
9metrics
 
 
 
?
regularization_losses
	variables

:layers
;non_trainable_variables
trainable_variables
<layer_metrics
=layer_regularization_losses
>metrics
\Z
VARIABLE_VALUEdense_349/kernel6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUE
XV
VARIABLE_VALUEdense_349/bias4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUE
 

0
1

0
1
?
regularization_losses
	variables

?layers
@non_trainable_variables
trainable_variables
Alayer_metrics
Blayer_regularization_losses
Cmetrics
\Z
VARIABLE_VALUEdense_350/kernel6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUE
XV
VARIABLE_VALUEdense_350/bias4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUE
 

 0
!1

 0
!1
?
"regularization_losses
#	variables

Dlayers
Enon_trainable_variables
$trainable_variables
Flayer_metrics
Glayer_regularization_losses
Hmetrics
HF
VARIABLE_VALUE	Adam/iter)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUE
LJ
VARIABLE_VALUEAdam/beta_1+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUE
LJ
VARIABLE_VALUEAdam/beta_2+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUE
JH
VARIABLE_VALUE
Adam/decay*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUE
ZX
VARIABLE_VALUEAdam/learning_rate2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUE
#
0
1
2
3
4
 
 
 

I0
J1
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
4
	Ktotal
	Lcount
M	variables
N	keras_api
D
	Ototal
	Pcount
Q
_fn_kwargs
R	variables
S	keras_api
OM
VARIABLE_VALUEtotal4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUE
OM
VARIABLE_VALUEcount4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUE

K0
L1

M	variables
QO
VARIABLE_VALUEtotal_14keras_api/metrics/1/total/.ATTRIBUTES/VARIABLE_VALUE
QO
VARIABLE_VALUEcount_14keras_api/metrics/1/count/.ATTRIBUTES/VARIABLE_VALUE
 

O0
P1

R	variables
}
VARIABLE_VALUEAdam/dense_348/kernel/mRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_348/bias/mPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
}
VARIABLE_VALUEAdam/dense_349/kernel/mRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_349/bias/mPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
}
VARIABLE_VALUEAdam/dense_350/kernel/mRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_350/bias/mPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUE
}
VARIABLE_VALUEAdam/dense_348/kernel/vRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_348/bias/vPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
}
VARIABLE_VALUEAdam/dense_349/kernel/vRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_349/bias/vPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
}
VARIABLE_VALUEAdam/dense_350/kernel/vRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
{y
VARIABLE_VALUEAdam/dense_350/bias/vPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUE
?
!serving_default_flatten_107_inputPlaceholder*/
_output_shapes
:?????????G*
dtype0*$
shape:?????????G
?
StatefulPartitionedCallStatefulPartitionedCall!serving_default_flatten_107_inputdense_348/kerneldense_348/biasdense_349/kerneldense_349/biasdense_350/kerneldense_350/bias*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *.
f)R'
%__inference_signature_wrapper_1510347
O
saver_filenamePlaceholder*
_output_shapes
: *
dtype0*
shape: 
?

StatefulPartitionedCall_1StatefulPartitionedCallsaver_filename$dense_348/kernel/Read/ReadVariableOp"dense_348/bias/Read/ReadVariableOp$dense_349/kernel/Read/ReadVariableOp"dense_349/bias/Read/ReadVariableOp$dense_350/kernel/Read/ReadVariableOp"dense_350/bias/Read/ReadVariableOpAdam/iter/Read/ReadVariableOpAdam/beta_1/Read/ReadVariableOpAdam/beta_2/Read/ReadVariableOpAdam/decay/Read/ReadVariableOp&Adam/learning_rate/Read/ReadVariableOptotal/Read/ReadVariableOpcount/Read/ReadVariableOptotal_1/Read/ReadVariableOpcount_1/Read/ReadVariableOp+Adam/dense_348/kernel/m/Read/ReadVariableOp)Adam/dense_348/bias/m/Read/ReadVariableOp+Adam/dense_349/kernel/m/Read/ReadVariableOp)Adam/dense_349/bias/m/Read/ReadVariableOp+Adam/dense_350/kernel/m/Read/ReadVariableOp)Adam/dense_350/bias/m/Read/ReadVariableOp+Adam/dense_348/kernel/v/Read/ReadVariableOp)Adam/dense_348/bias/v/Read/ReadVariableOp+Adam/dense_349/kernel/v/Read/ReadVariableOp)Adam/dense_349/bias/v/Read/ReadVariableOp+Adam/dense_350/kernel/v/Read/ReadVariableOp)Adam/dense_350/bias/v/Read/ReadVariableOpConst*(
Tin!
2	*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *)
f$R"
 __inference__traced_save_1510646
?
StatefulPartitionedCall_2StatefulPartitionedCallsaver_filenamedense_348/kerneldense_348/biasdense_349/kerneldense_349/biasdense_350/kerneldense_350/bias	Adam/iterAdam/beta_1Adam/beta_2
Adam/decayAdam/learning_ratetotalcounttotal_1count_1Adam/dense_348/kernel/mAdam/dense_348/bias/mAdam/dense_349/kernel/mAdam/dense_349/bias/mAdam/dense_350/kernel/mAdam/dense_350/bias/mAdam/dense_348/kernel/vAdam/dense_348/bias/vAdam/dense_349/kernel/vAdam/dense_349/bias/vAdam/dense_350/kernel/vAdam/dense_350/bias/v*'
Tin 
2*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *,
f'R%
#__inference__traced_restore_1510737??
?
?
+__inference_dense_348_layer_call_fn_1510475

inputs
unknown
	unknown_0
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_348_layer_call_and_return_conditional_losses_15101212
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*/
_input_shapes
:??????????::22
StatefulPartitionedCallStatefulPartitionedCall:P L
(
_output_shapes
:??????????
 
_user_specified_nameinputs
?
e
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510492

inputs

identity_1Z
IdentityIdentityinputs*
T0*'
_output_shapes
:?????????@2

Identityi

Identity_1IdentityIdentity:output:0*
T0*'
_output_shapes
:?????????@2

Identity_1"!

identity_1Identity_1:output:0*&
_input_shapes
:?????????@:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510305

inputs
dense_348_1510288
dense_348_1510290
dense_349_1510294
dense_349_1510296
dense_350_1510299
dense_350_1510301
identity??!dense_348/StatefulPartitionedCall?!dense_349/StatefulPartitionedCall?!dense_350/StatefulPartitionedCall?
flatten_107/PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *(
_output_shapes
:??????????* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *Q
fLRJ
H__inference_flatten_107_layer_call_and_return_conditional_losses_15101022
flatten_107/PartitionedCall?
!dense_348/StatefulPartitionedCallStatefulPartitionedCall$flatten_107/PartitionedCall:output:0dense_348_1510288dense_348_1510290*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_348_layer_call_and_return_conditional_losses_15101212#
!dense_348/StatefulPartitionedCall?
dropout_65/PartitionedCallPartitionedCall*dense_348/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101542
dropout_65/PartitionedCall?
!dense_349/StatefulPartitionedCallStatefulPartitionedCall#dropout_65/PartitionedCall:output:0dense_349_1510294dense_349_1510296*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_349_layer_call_and_return_conditional_losses_15101782#
!dense_349/StatefulPartitionedCall?
!dense_350/StatefulPartitionedCallStatefulPartitionedCall*dense_349/StatefulPartitionedCall:output:0dense_350_1510299dense_350_1510301*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_350_layer_call_and_return_conditional_losses_15102052#
!dense_350/StatefulPartitionedCall?
IdentityIdentity*dense_350/StatefulPartitionedCall:output:0"^dense_348/StatefulPartitionedCall"^dense_349/StatefulPartitionedCall"^dense_350/StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2F
!dense_348/StatefulPartitionedCall!dense_348/StatefulPartitionedCall2F
!dense_349/StatefulPartitionedCall!dense_349/StatefulPartitionedCall2F
!dense_350/StatefulPartitionedCall!dense_350/StatefulPartitionedCall:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?+
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510382

inputs,
(dense_348_matmul_readvariableop_resource-
)dense_348_biasadd_readvariableop_resource,
(dense_349_matmul_readvariableop_resource-
)dense_349_biasadd_readvariableop_resource,
(dense_350_matmul_readvariableop_resource-
)dense_350_biasadd_readvariableop_resource
identity?? dense_348/BiasAdd/ReadVariableOp?dense_348/MatMul/ReadVariableOp? dense_349/BiasAdd/ReadVariableOp?dense_349/MatMul/ReadVariableOp? dense_350/BiasAdd/ReadVariableOp?dense_350/MatMul/ReadVariableOpw
flatten_107/ConstConst*
_output_shapes
:*
dtype0*
valueB"?????  2
flatten_107/Const?
flatten_107/ReshapeReshapeinputsflatten_107/Const:output:0*
T0*(
_output_shapes
:??????????2
flatten_107/Reshape?
dense_348/MatMul/ReadVariableOpReadVariableOp(dense_348_matmul_readvariableop_resource*
_output_shapes
:	?@*
dtype02!
dense_348/MatMul/ReadVariableOp?
dense_348/MatMulMatMulflatten_107/Reshape:output:0'dense_348/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
dense_348/MatMul?
 dense_348/BiasAdd/ReadVariableOpReadVariableOp)dense_348_biasadd_readvariableop_resource*
_output_shapes
:@*
dtype02"
 dense_348/BiasAdd/ReadVariableOp?
dense_348/BiasAddBiasAdddense_348/MatMul:product:0(dense_348/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
dense_348/BiasAddv
dense_348/ReluReludense_348/BiasAdd:output:0*
T0*'
_output_shapes
:?????????@2
dense_348/Reluy
dropout_65/dropout/ConstConst*
_output_shapes
: *
dtype0*
valueB
 *  ??2
dropout_65/dropout/Const?
dropout_65/dropout/MulMuldense_348/Relu:activations:0!dropout_65/dropout/Const:output:0*
T0*'
_output_shapes
:?????????@2
dropout_65/dropout/Mul?
dropout_65/dropout/ShapeShapedense_348/Relu:activations:0*
T0*
_output_shapes
:2
dropout_65/dropout/Shape?
/dropout_65/dropout/random_uniform/RandomUniformRandomUniform!dropout_65/dropout/Shape:output:0*
T0*'
_output_shapes
:?????????@*
dtype021
/dropout_65/dropout/random_uniform/RandomUniform?
!dropout_65/dropout/GreaterEqual/yConst*
_output_shapes
: *
dtype0*
valueB
 *??L>2#
!dropout_65/dropout/GreaterEqual/y?
dropout_65/dropout/GreaterEqualGreaterEqual8dropout_65/dropout/random_uniform/RandomUniform:output:0*dropout_65/dropout/GreaterEqual/y:output:0*
T0*'
_output_shapes
:?????????@2!
dropout_65/dropout/GreaterEqual?
dropout_65/dropout/CastCast#dropout_65/dropout/GreaterEqual:z:0*

DstT0*

SrcT0
*'
_output_shapes
:?????????@2
dropout_65/dropout/Cast?
dropout_65/dropout/Mul_1Muldropout_65/dropout/Mul:z:0dropout_65/dropout/Cast:y:0*
T0*'
_output_shapes
:?????????@2
dropout_65/dropout/Mul_1?
dense_349/MatMul/ReadVariableOpReadVariableOp(dense_349_matmul_readvariableop_resource*
_output_shapes

:@*
dtype02!
dense_349/MatMul/ReadVariableOp?
dense_349/MatMulMatMuldropout_65/dropout/Mul_1:z:0'dense_349/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_349/MatMul?
 dense_349/BiasAdd/ReadVariableOpReadVariableOp)dense_349_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02"
 dense_349/BiasAdd/ReadVariableOp?
dense_349/BiasAddBiasAdddense_349/MatMul:product:0(dense_349/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_349/BiasAddv
dense_349/ReluReludense_349/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2
dense_349/Relu?
dense_350/MatMul/ReadVariableOpReadVariableOp(dense_350_matmul_readvariableop_resource*
_output_shapes

:*
dtype02!
dense_350/MatMul/ReadVariableOp?
dense_350/MatMulMatMuldense_349/Relu:activations:0'dense_350/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_350/MatMul?
 dense_350/BiasAdd/ReadVariableOpReadVariableOp)dense_350_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02"
 dense_350/BiasAdd/ReadVariableOp?
dense_350/BiasAddBiasAdddense_350/MatMul:product:0(dense_350/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_350/BiasAdd
dense_350/SoftmaxSoftmaxdense_350/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2
dense_350/Softmax?
IdentityIdentitydense_350/Softmax:softmax:0!^dense_348/BiasAdd/ReadVariableOp ^dense_348/MatMul/ReadVariableOp!^dense_349/BiasAdd/ReadVariableOp ^dense_349/MatMul/ReadVariableOp!^dense_350/BiasAdd/ReadVariableOp ^dense_350/MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2D
 dense_348/BiasAdd/ReadVariableOp dense_348/BiasAdd/ReadVariableOp2B
dense_348/MatMul/ReadVariableOpdense_348/MatMul/ReadVariableOp2D
 dense_349/BiasAdd/ReadVariableOp dense_349/BiasAdd/ReadVariableOp2B
dense_349/MatMul/ReadVariableOpdense_349/MatMul/ReadVariableOp2D
 dense_350/BiasAdd/ReadVariableOp dense_350/BiasAdd/ReadVariableOp2B
dense_350/MatMul/ReadVariableOpdense_350/MatMul/ReadVariableOp:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?	
?
F__inference_dense_349_layer_call_and_return_conditional_losses_1510178

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:@*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2	
BiasAddX
ReluReluBiasAdd:output:0*
T0*'
_output_shapes
:?????????2
Relu?
IdentityIdentityRelu:activations:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????@::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
?
0__inference_sequential_109_layer_call_fn_1510282
flatten_107_input
unknown
	unknown_0
	unknown_1
	unknown_2
	unknown_3
	unknown_4
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallflatten_107_inputunknown	unknown_0	unknown_1	unknown_2	unknown_3	unknown_4*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *T
fORM
K__inference_sequential_109_layer_call_and_return_conditional_losses_15102672
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::22
StatefulPartitionedCallStatefulPartitionedCall:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?	
?
F__inference_dense_349_layer_call_and_return_conditional_losses_1510513

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:@*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2	
BiasAddX
ReluReluBiasAdd:output:0*
T0*'
_output_shapes
:?????????2
Relu?
IdentityIdentityRelu:activations:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????@::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
d
H__inference_flatten_107_layer_call_and_return_conditional_losses_1510450

inputs
identity_
ConstConst*
_output_shapes
:*
dtype0*
valueB"?????  2
Consth
ReshapeReshapeinputsConst:output:0*
T0*(
_output_shapes
:??????????2	
Reshapee
IdentityIdentityReshape:output:0*
T0*(
_output_shapes
:??????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????G:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?
?
%__inference_signature_wrapper_1510347
flatten_107_input
unknown
	unknown_0
	unknown_1
	unknown_2
	unknown_3
	unknown_4
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallflatten_107_inputunknown	unknown_0	unknown_1	unknown_2	unknown_3	unknown_4*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *+
f&R$
"__inference__wrapped_model_15100922
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::22
StatefulPartitionedCallStatefulPartitionedCall:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?
?
+__inference_dense_349_layer_call_fn_1510522

inputs
unknown
	unknown_0
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_349_layer_call_and_return_conditional_losses_15101782
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????@::22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
f
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510149

inputs
identity?c
dropout/ConstConst*
_output_shapes
: *
dtype0*
valueB
 *  ??2
dropout/Consts
dropout/MulMulinputsdropout/Const:output:0*
T0*'
_output_shapes
:?????????@2
dropout/MulT
dropout/ShapeShapeinputs*
T0*
_output_shapes
:2
dropout/Shape?
$dropout/random_uniform/RandomUniformRandomUniformdropout/Shape:output:0*
T0*'
_output_shapes
:?????????@*
dtype02&
$dropout/random_uniform/RandomUniformu
dropout/GreaterEqual/yConst*
_output_shapes
: *
dtype0*
valueB
 *??L>2
dropout/GreaterEqual/y?
dropout/GreaterEqualGreaterEqual-dropout/random_uniform/RandomUniform:output:0dropout/GreaterEqual/y:output:0*
T0*'
_output_shapes
:?????????@2
dropout/GreaterEqual
dropout/CastCastdropout/GreaterEqual:z:0*

DstT0*

SrcT0
*'
_output_shapes
:?????????@2
dropout/Castz
dropout/Mul_1Muldropout/Mul:z:0dropout/Cast:y:0*
T0*'
_output_shapes
:?????????@2
dropout/Mul_1e
IdentityIdentitydropout/Mul_1:z:0*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*&
_input_shapes
:?????????@:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?=
?
 __inference__traced_save_1510646
file_prefix/
+savev2_dense_348_kernel_read_readvariableop-
)savev2_dense_348_bias_read_readvariableop/
+savev2_dense_349_kernel_read_readvariableop-
)savev2_dense_349_bias_read_readvariableop/
+savev2_dense_350_kernel_read_readvariableop-
)savev2_dense_350_bias_read_readvariableop(
$savev2_adam_iter_read_readvariableop	*
&savev2_adam_beta_1_read_readvariableop*
&savev2_adam_beta_2_read_readvariableop)
%savev2_adam_decay_read_readvariableop1
-savev2_adam_learning_rate_read_readvariableop$
 savev2_total_read_readvariableop$
 savev2_count_read_readvariableop&
"savev2_total_1_read_readvariableop&
"savev2_count_1_read_readvariableop6
2savev2_adam_dense_348_kernel_m_read_readvariableop4
0savev2_adam_dense_348_bias_m_read_readvariableop6
2savev2_adam_dense_349_kernel_m_read_readvariableop4
0savev2_adam_dense_349_bias_m_read_readvariableop6
2savev2_adam_dense_350_kernel_m_read_readvariableop4
0savev2_adam_dense_350_bias_m_read_readvariableop6
2savev2_adam_dense_348_kernel_v_read_readvariableop4
0savev2_adam_dense_348_bias_v_read_readvariableop6
2savev2_adam_dense_349_kernel_v_read_readvariableop4
0savev2_adam_dense_349_bias_v_read_readvariableop6
2savev2_adam_dense_350_kernel_v_read_readvariableop4
0savev2_adam_dense_350_bias_v_read_readvariableop
savev2_const

identity_1??MergeV2Checkpoints?
StaticRegexFullMatchStaticRegexFullMatchfile_prefix"/device:CPU:**
_output_shapes
: *
pattern
^s3://.*2
StaticRegexFullMatchc
ConstConst"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B.part2
Constl
Const_1Const"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B
_temp/part2	
Const_1?
SelectSelectStaticRegexFullMatch:output:0Const:output:0Const_1:output:0"/device:CPU:**
T0*
_output_shapes
: 2
Selectt

StringJoin
StringJoinfile_prefixSelect:output:0"/device:CPU:**
N*
_output_shapes
: 2

StringJoinZ

num_shardsConst*
_output_shapes
: *
dtype0*
value	B :2

num_shards
ShardedFilename/shardConst"/device:CPU:0*
_output_shapes
: *
dtype0*
value	B : 2
ShardedFilename/shard?
ShardedFilenameShardedFilenameStringJoin:output:0ShardedFilename/shard:output:0num_shards:output:0"/device:CPU:0*
_output_shapes
: 2
ShardedFilename?
SaveV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*?
value?B?B6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/1/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/1/count/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPH2
SaveV2/tensor_names?
SaveV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*K
valueBB@B B B B B B B B B B B B B B B B B B B B B B B B B B B B 2
SaveV2/shape_and_slices?
SaveV2SaveV2ShardedFilename:filename:0SaveV2/tensor_names:output:0 SaveV2/shape_and_slices:output:0+savev2_dense_348_kernel_read_readvariableop)savev2_dense_348_bias_read_readvariableop+savev2_dense_349_kernel_read_readvariableop)savev2_dense_349_bias_read_readvariableop+savev2_dense_350_kernel_read_readvariableop)savev2_dense_350_bias_read_readvariableop$savev2_adam_iter_read_readvariableop&savev2_adam_beta_1_read_readvariableop&savev2_adam_beta_2_read_readvariableop%savev2_adam_decay_read_readvariableop-savev2_adam_learning_rate_read_readvariableop savev2_total_read_readvariableop savev2_count_read_readvariableop"savev2_total_1_read_readvariableop"savev2_count_1_read_readvariableop2savev2_adam_dense_348_kernel_m_read_readvariableop0savev2_adam_dense_348_bias_m_read_readvariableop2savev2_adam_dense_349_kernel_m_read_readvariableop0savev2_adam_dense_349_bias_m_read_readvariableop2savev2_adam_dense_350_kernel_m_read_readvariableop0savev2_adam_dense_350_bias_m_read_readvariableop2savev2_adam_dense_348_kernel_v_read_readvariableop0savev2_adam_dense_348_bias_v_read_readvariableop2savev2_adam_dense_349_kernel_v_read_readvariableop0savev2_adam_dense_349_bias_v_read_readvariableop2savev2_adam_dense_350_kernel_v_read_readvariableop0savev2_adam_dense_350_bias_v_read_readvariableopsavev2_const"/device:CPU:0*
_output_shapes
 **
dtypes 
2	2
SaveV2?
&MergeV2Checkpoints/checkpoint_prefixesPackShardedFilename:filename:0^SaveV2"/device:CPU:0*
N*
T0*
_output_shapes
:2(
&MergeV2Checkpoints/checkpoint_prefixes?
MergeV2CheckpointsMergeV2Checkpoints/MergeV2Checkpoints/checkpoint_prefixes:output:0file_prefix"/device:CPU:0*
_output_shapes
 2
MergeV2Checkpointsr
IdentityIdentityfile_prefix^MergeV2Checkpoints"/device:CPU:0*
T0*
_output_shapes
: 2

Identitym

Identity_1IdentityIdentity:output:0^MergeV2Checkpoints*
T0*
_output_shapes
: 2

Identity_1"!

identity_1Identity_1:output:0*?
_input_shapes?
?: :	?@:@:@:::: : : : : : : : : :	?@:@:@::::	?@:@:@:::: 2(
MergeV2CheckpointsMergeV2Checkpoints:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix:%!

_output_shapes
:	?@: 

_output_shapes
:@:$ 

_output_shapes

:@: 

_output_shapes
::$ 

_output_shapes

:: 

_output_shapes
::

_output_shapes
: :

_output_shapes
: :	

_output_shapes
: :


_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :%!

_output_shapes
:	?@: 

_output_shapes
:@:$ 

_output_shapes

:@: 

_output_shapes
::$ 

_output_shapes

:: 

_output_shapes
::%!

_output_shapes
:	?@: 

_output_shapes
:@:$ 

_output_shapes

:@: 

_output_shapes
::$ 

_output_shapes

:: 

_output_shapes
::

_output_shapes
: 
?
e
,__inference_dropout_65_layer_call_fn_1510497

inputs
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101492
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*&
_input_shapes
:?????????@22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510243
flatten_107_input
dense_348_1510226
dense_348_1510228
dense_349_1510232
dense_349_1510234
dense_350_1510237
dense_350_1510239
identity??!dense_348/StatefulPartitionedCall?!dense_349/StatefulPartitionedCall?!dense_350/StatefulPartitionedCall?
flatten_107/PartitionedCallPartitionedCallflatten_107_input*
Tin
2*
Tout
2*
_collective_manager_ids
 *(
_output_shapes
:??????????* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *Q
fLRJ
H__inference_flatten_107_layer_call_and_return_conditional_losses_15101022
flatten_107/PartitionedCall?
!dense_348/StatefulPartitionedCallStatefulPartitionedCall$flatten_107/PartitionedCall:output:0dense_348_1510226dense_348_1510228*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_348_layer_call_and_return_conditional_losses_15101212#
!dense_348/StatefulPartitionedCall?
dropout_65/PartitionedCallPartitionedCall*dense_348/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101542
dropout_65/PartitionedCall?
!dense_349/StatefulPartitionedCallStatefulPartitionedCall#dropout_65/PartitionedCall:output:0dense_349_1510232dense_349_1510234*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_349_layer_call_and_return_conditional_losses_15101782#
!dense_349/StatefulPartitionedCall?
!dense_350/StatefulPartitionedCallStatefulPartitionedCall*dense_349/StatefulPartitionedCall:output:0dense_350_1510237dense_350_1510239*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_350_layer_call_and_return_conditional_losses_15102052#
!dense_350/StatefulPartitionedCall?
IdentityIdentity*dense_350/StatefulPartitionedCall:output:0"^dense_348/StatefulPartitionedCall"^dense_349/StatefulPartitionedCall"^dense_350/StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2F
!dense_348/StatefulPartitionedCall!dense_348/StatefulPartitionedCall2F
!dense_349/StatefulPartitionedCall!dense_349/StatefulPartitionedCall2F
!dense_350/StatefulPartitionedCall!dense_350/StatefulPartitionedCall:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?
?
+__inference_dense_350_layer_call_fn_1510542

inputs
unknown
	unknown_0
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_350_layer_call_and_return_conditional_losses_15102052
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????::22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:?????????
 
_user_specified_nameinputs
?
f
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510487

inputs
identity?c
dropout/ConstConst*
_output_shapes
: *
dtype0*
valueB
 *  ??2
dropout/Consts
dropout/MulMulinputsdropout/Const:output:0*
T0*'
_output_shapes
:?????????@2
dropout/MulT
dropout/ShapeShapeinputs*
T0*
_output_shapes
:2
dropout/Shape?
$dropout/random_uniform/RandomUniformRandomUniformdropout/Shape:output:0*
T0*'
_output_shapes
:?????????@*
dtype02&
$dropout/random_uniform/RandomUniformu
dropout/GreaterEqual/yConst*
_output_shapes
: *
dtype0*
valueB
 *??L>2
dropout/GreaterEqual/y?
dropout/GreaterEqualGreaterEqual-dropout/random_uniform/RandomUniform:output:0dropout/GreaterEqual/y:output:0*
T0*'
_output_shapes
:?????????@2
dropout/GreaterEqual
dropout/CastCastdropout/GreaterEqual:z:0*

DstT0*

SrcT0
*'
_output_shapes
:?????????@2
dropout/Castz
dropout/Mul_1Muldropout/Mul:z:0dropout/Cast:y:0*
T0*'
_output_shapes
:?????????@2
dropout/Mul_1e
IdentityIdentitydropout/Mul_1:z:0*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*&
_input_shapes
:?????????@:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
?
0__inference_sequential_109_layer_call_fn_1510444

inputs
unknown
	unknown_0
	unknown_1
	unknown_2
	unknown_3
	unknown_4
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0	unknown_1	unknown_2	unknown_3	unknown_4*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *T
fORM
K__inference_sequential_109_layer_call_and_return_conditional_losses_15103052
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::22
StatefulPartitionedCallStatefulPartitionedCall:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?
?
0__inference_sequential_109_layer_call_fn_1510427

inputs
unknown
	unknown_0
	unknown_1
	unknown_2
	unknown_3
	unknown_4
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0	unknown_1	unknown_2	unknown_3	unknown_4*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *T
fORM
K__inference_sequential_109_layer_call_and_return_conditional_losses_15102672
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::22
StatefulPartitionedCallStatefulPartitionedCall:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?
H
,__inference_dropout_65_layer_call_fn_1510502

inputs
identity?
PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101542
PartitionedCalll
IdentityIdentityPartitionedCall:output:0*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*&
_input_shapes
:?????????@:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?	
?
F__inference_dense_348_layer_call_and_return_conditional_losses_1510466

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes
:	?@*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:@*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2	
BiasAddX
ReluReluBiasAdd:output:0*
T0*'
_output_shapes
:?????????@2
Relu?
IdentityIdentityRelu:activations:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*/
_input_shapes
:??????????::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:P L
(
_output_shapes
:??????????
 
_user_specified_nameinputs
?s
?
#__inference__traced_restore_1510737
file_prefix%
!assignvariableop_dense_348_kernel%
!assignvariableop_1_dense_348_bias'
#assignvariableop_2_dense_349_kernel%
!assignvariableop_3_dense_349_bias'
#assignvariableop_4_dense_350_kernel%
!assignvariableop_5_dense_350_bias 
assignvariableop_6_adam_iter"
assignvariableop_7_adam_beta_1"
assignvariableop_8_adam_beta_2!
assignvariableop_9_adam_decay*
&assignvariableop_10_adam_learning_rate
assignvariableop_11_total
assignvariableop_12_count
assignvariableop_13_total_1
assignvariableop_14_count_1/
+assignvariableop_15_adam_dense_348_kernel_m-
)assignvariableop_16_adam_dense_348_bias_m/
+assignvariableop_17_adam_dense_349_kernel_m-
)assignvariableop_18_adam_dense_349_bias_m/
+assignvariableop_19_adam_dense_350_kernel_m-
)assignvariableop_20_adam_dense_350_bias_m/
+assignvariableop_21_adam_dense_348_kernel_v-
)assignvariableop_22_adam_dense_348_bias_v/
+assignvariableop_23_adam_dense_349_kernel_v-
)assignvariableop_24_adam_dense_349_bias_v/
+assignvariableop_25_adam_dense_350_kernel_v-
)assignvariableop_26_adam_dense_350_bias_v
identity_28??AssignVariableOp?AssignVariableOp_1?AssignVariableOp_10?AssignVariableOp_11?AssignVariableOp_12?AssignVariableOp_13?AssignVariableOp_14?AssignVariableOp_15?AssignVariableOp_16?AssignVariableOp_17?AssignVariableOp_18?AssignVariableOp_19?AssignVariableOp_2?AssignVariableOp_20?AssignVariableOp_21?AssignVariableOp_22?AssignVariableOp_23?AssignVariableOp_24?AssignVariableOp_25?AssignVariableOp_26?AssignVariableOp_3?AssignVariableOp_4?AssignVariableOp_5?AssignVariableOp_6?AssignVariableOp_7?AssignVariableOp_8?AssignVariableOp_9?
RestoreV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*?
value?B?B6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-1/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-1/bias/.ATTRIBUTES/VARIABLE_VALUEB6layer_with_weights-2/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-2/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_1/.ATTRIBUTES/VARIABLE_VALUEB+optimizer/beta_2/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/1/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/1/count/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/m/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-0/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-0/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-1/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-1/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBRlayer_with_weights-2/kernel/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEBPlayer_with_weights-2/bias/.OPTIMIZER_SLOT/optimizer/v/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPH2
RestoreV2/tensor_names?
RestoreV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*K
valueBB@B B B B B B B B B B B B B B B B B B B B B B B B B B B B 2
RestoreV2/shape_and_slices?
	RestoreV2	RestoreV2file_prefixRestoreV2/tensor_names:output:0#RestoreV2/shape_and_slices:output:0"/device:CPU:0*?
_output_shapesr
p::::::::::::::::::::::::::::**
dtypes 
2	2
	RestoreV2g
IdentityIdentityRestoreV2:tensors:0"/device:CPU:0*
T0*
_output_shapes
:2

Identity?
AssignVariableOpAssignVariableOp!assignvariableop_dense_348_kernelIdentity:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOpk

Identity_1IdentityRestoreV2:tensors:1"/device:CPU:0*
T0*
_output_shapes
:2

Identity_1?
AssignVariableOp_1AssignVariableOp!assignvariableop_1_dense_348_biasIdentity_1:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_1k

Identity_2IdentityRestoreV2:tensors:2"/device:CPU:0*
T0*
_output_shapes
:2

Identity_2?
AssignVariableOp_2AssignVariableOp#assignvariableop_2_dense_349_kernelIdentity_2:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_2k

Identity_3IdentityRestoreV2:tensors:3"/device:CPU:0*
T0*
_output_shapes
:2

Identity_3?
AssignVariableOp_3AssignVariableOp!assignvariableop_3_dense_349_biasIdentity_3:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_3k

Identity_4IdentityRestoreV2:tensors:4"/device:CPU:0*
T0*
_output_shapes
:2

Identity_4?
AssignVariableOp_4AssignVariableOp#assignvariableop_4_dense_350_kernelIdentity_4:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_4k

Identity_5IdentityRestoreV2:tensors:5"/device:CPU:0*
T0*
_output_shapes
:2

Identity_5?
AssignVariableOp_5AssignVariableOp!assignvariableop_5_dense_350_biasIdentity_5:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_5k

Identity_6IdentityRestoreV2:tensors:6"/device:CPU:0*
T0	*
_output_shapes
:2

Identity_6?
AssignVariableOp_6AssignVariableOpassignvariableop_6_adam_iterIdentity_6:output:0"/device:CPU:0*
_output_shapes
 *
dtype0	2
AssignVariableOp_6k

Identity_7IdentityRestoreV2:tensors:7"/device:CPU:0*
T0*
_output_shapes
:2

Identity_7?
AssignVariableOp_7AssignVariableOpassignvariableop_7_adam_beta_1Identity_7:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_7k

Identity_8IdentityRestoreV2:tensors:8"/device:CPU:0*
T0*
_output_shapes
:2

Identity_8?
AssignVariableOp_8AssignVariableOpassignvariableop_8_adam_beta_2Identity_8:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_8k

Identity_9IdentityRestoreV2:tensors:9"/device:CPU:0*
T0*
_output_shapes
:2

Identity_9?
AssignVariableOp_9AssignVariableOpassignvariableop_9_adam_decayIdentity_9:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_9n
Identity_10IdentityRestoreV2:tensors:10"/device:CPU:0*
T0*
_output_shapes
:2
Identity_10?
AssignVariableOp_10AssignVariableOp&assignvariableop_10_adam_learning_rateIdentity_10:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_10n
Identity_11IdentityRestoreV2:tensors:11"/device:CPU:0*
T0*
_output_shapes
:2
Identity_11?
AssignVariableOp_11AssignVariableOpassignvariableop_11_totalIdentity_11:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_11n
Identity_12IdentityRestoreV2:tensors:12"/device:CPU:0*
T0*
_output_shapes
:2
Identity_12?
AssignVariableOp_12AssignVariableOpassignvariableop_12_countIdentity_12:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_12n
Identity_13IdentityRestoreV2:tensors:13"/device:CPU:0*
T0*
_output_shapes
:2
Identity_13?
AssignVariableOp_13AssignVariableOpassignvariableop_13_total_1Identity_13:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_13n
Identity_14IdentityRestoreV2:tensors:14"/device:CPU:0*
T0*
_output_shapes
:2
Identity_14?
AssignVariableOp_14AssignVariableOpassignvariableop_14_count_1Identity_14:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_14n
Identity_15IdentityRestoreV2:tensors:15"/device:CPU:0*
T0*
_output_shapes
:2
Identity_15?
AssignVariableOp_15AssignVariableOp+assignvariableop_15_adam_dense_348_kernel_mIdentity_15:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_15n
Identity_16IdentityRestoreV2:tensors:16"/device:CPU:0*
T0*
_output_shapes
:2
Identity_16?
AssignVariableOp_16AssignVariableOp)assignvariableop_16_adam_dense_348_bias_mIdentity_16:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_16n
Identity_17IdentityRestoreV2:tensors:17"/device:CPU:0*
T0*
_output_shapes
:2
Identity_17?
AssignVariableOp_17AssignVariableOp+assignvariableop_17_adam_dense_349_kernel_mIdentity_17:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_17n
Identity_18IdentityRestoreV2:tensors:18"/device:CPU:0*
T0*
_output_shapes
:2
Identity_18?
AssignVariableOp_18AssignVariableOp)assignvariableop_18_adam_dense_349_bias_mIdentity_18:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_18n
Identity_19IdentityRestoreV2:tensors:19"/device:CPU:0*
T0*
_output_shapes
:2
Identity_19?
AssignVariableOp_19AssignVariableOp+assignvariableop_19_adam_dense_350_kernel_mIdentity_19:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_19n
Identity_20IdentityRestoreV2:tensors:20"/device:CPU:0*
T0*
_output_shapes
:2
Identity_20?
AssignVariableOp_20AssignVariableOp)assignvariableop_20_adam_dense_350_bias_mIdentity_20:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_20n
Identity_21IdentityRestoreV2:tensors:21"/device:CPU:0*
T0*
_output_shapes
:2
Identity_21?
AssignVariableOp_21AssignVariableOp+assignvariableop_21_adam_dense_348_kernel_vIdentity_21:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_21n
Identity_22IdentityRestoreV2:tensors:22"/device:CPU:0*
T0*
_output_shapes
:2
Identity_22?
AssignVariableOp_22AssignVariableOp)assignvariableop_22_adam_dense_348_bias_vIdentity_22:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_22n
Identity_23IdentityRestoreV2:tensors:23"/device:CPU:0*
T0*
_output_shapes
:2
Identity_23?
AssignVariableOp_23AssignVariableOp+assignvariableop_23_adam_dense_349_kernel_vIdentity_23:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_23n
Identity_24IdentityRestoreV2:tensors:24"/device:CPU:0*
T0*
_output_shapes
:2
Identity_24?
AssignVariableOp_24AssignVariableOp)assignvariableop_24_adam_dense_349_bias_vIdentity_24:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_24n
Identity_25IdentityRestoreV2:tensors:25"/device:CPU:0*
T0*
_output_shapes
:2
Identity_25?
AssignVariableOp_25AssignVariableOp+assignvariableop_25_adam_dense_350_kernel_vIdentity_25:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_25n
Identity_26IdentityRestoreV2:tensors:26"/device:CPU:0*
T0*
_output_shapes
:2
Identity_26?
AssignVariableOp_26AssignVariableOp)assignvariableop_26_adam_dense_350_bias_vIdentity_26:output:0"/device:CPU:0*
_output_shapes
 *
dtype02
AssignVariableOp_269
NoOpNoOp"/device:CPU:0*
_output_shapes
 2
NoOp?
Identity_27Identityfile_prefix^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_10^AssignVariableOp_11^AssignVariableOp_12^AssignVariableOp_13^AssignVariableOp_14^AssignVariableOp_15^AssignVariableOp_16^AssignVariableOp_17^AssignVariableOp_18^AssignVariableOp_19^AssignVariableOp_2^AssignVariableOp_20^AssignVariableOp_21^AssignVariableOp_22^AssignVariableOp_23^AssignVariableOp_24^AssignVariableOp_25^AssignVariableOp_26^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7^AssignVariableOp_8^AssignVariableOp_9^NoOp"/device:CPU:0*
T0*
_output_shapes
: 2
Identity_27?
Identity_28IdentityIdentity_27:output:0^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_10^AssignVariableOp_11^AssignVariableOp_12^AssignVariableOp_13^AssignVariableOp_14^AssignVariableOp_15^AssignVariableOp_16^AssignVariableOp_17^AssignVariableOp_18^AssignVariableOp_19^AssignVariableOp_2^AssignVariableOp_20^AssignVariableOp_21^AssignVariableOp_22^AssignVariableOp_23^AssignVariableOp_24^AssignVariableOp_25^AssignVariableOp_26^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7^AssignVariableOp_8^AssignVariableOp_9*
T0*
_output_shapes
: 2
Identity_28"#
identity_28Identity_28:output:0*?
_input_shapesp
n: :::::::::::::::::::::::::::2$
AssignVariableOpAssignVariableOp2(
AssignVariableOp_1AssignVariableOp_12*
AssignVariableOp_10AssignVariableOp_102*
AssignVariableOp_11AssignVariableOp_112*
AssignVariableOp_12AssignVariableOp_122*
AssignVariableOp_13AssignVariableOp_132*
AssignVariableOp_14AssignVariableOp_142*
AssignVariableOp_15AssignVariableOp_152*
AssignVariableOp_16AssignVariableOp_162*
AssignVariableOp_17AssignVariableOp_172*
AssignVariableOp_18AssignVariableOp_182*
AssignVariableOp_19AssignVariableOp_192(
AssignVariableOp_2AssignVariableOp_22*
AssignVariableOp_20AssignVariableOp_202*
AssignVariableOp_21AssignVariableOp_212*
AssignVariableOp_22AssignVariableOp_222*
AssignVariableOp_23AssignVariableOp_232*
AssignVariableOp_24AssignVariableOp_242*
AssignVariableOp_25AssignVariableOp_252*
AssignVariableOp_26AssignVariableOp_262(
AssignVariableOp_3AssignVariableOp_32(
AssignVariableOp_4AssignVariableOp_42(
AssignVariableOp_5AssignVariableOp_52(
AssignVariableOp_6AssignVariableOp_62(
AssignVariableOp_7AssignVariableOp_72(
AssignVariableOp_8AssignVariableOp_82(
AssignVariableOp_9AssignVariableOp_9:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix
?	
?
F__inference_dense_350_layer_call_and_return_conditional_losses_1510533

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2	
BiasAdda
SoftmaxSoftmaxBiasAdd:output:0*
T0*'
_output_shapes
:?????????2	
Softmax?
IdentityIdentitySoftmax:softmax:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:O K
'
_output_shapes
:?????????
 
_user_specified_nameinputs
?
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510222
flatten_107_input
dense_348_1510132
dense_348_1510134
dense_349_1510189
dense_349_1510191
dense_350_1510216
dense_350_1510218
identity??!dense_348/StatefulPartitionedCall?!dense_349/StatefulPartitionedCall?!dense_350/StatefulPartitionedCall?"dropout_65/StatefulPartitionedCall?
flatten_107/PartitionedCallPartitionedCallflatten_107_input*
Tin
2*
Tout
2*
_collective_manager_ids
 *(
_output_shapes
:??????????* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *Q
fLRJ
H__inference_flatten_107_layer_call_and_return_conditional_losses_15101022
flatten_107/PartitionedCall?
!dense_348/StatefulPartitionedCallStatefulPartitionedCall$flatten_107/PartitionedCall:output:0dense_348_1510132dense_348_1510134*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_348_layer_call_and_return_conditional_losses_15101212#
!dense_348/StatefulPartitionedCall?
"dropout_65/StatefulPartitionedCallStatefulPartitionedCall*dense_348/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101492$
"dropout_65/StatefulPartitionedCall?
!dense_349/StatefulPartitionedCallStatefulPartitionedCall+dropout_65/StatefulPartitionedCall:output:0dense_349_1510189dense_349_1510191*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_349_layer_call_and_return_conditional_losses_15101782#
!dense_349/StatefulPartitionedCall?
!dense_350/StatefulPartitionedCallStatefulPartitionedCall*dense_349/StatefulPartitionedCall:output:0dense_350_1510216dense_350_1510218*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_350_layer_call_and_return_conditional_losses_15102052#
!dense_350/StatefulPartitionedCall?
IdentityIdentity*dense_350/StatefulPartitionedCall:output:0"^dense_348/StatefulPartitionedCall"^dense_349/StatefulPartitionedCall"^dense_350/StatefulPartitionedCall#^dropout_65/StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2F
!dense_348/StatefulPartitionedCall!dense_348/StatefulPartitionedCall2F
!dense_349/StatefulPartitionedCall!dense_349/StatefulPartitionedCall2F
!dense_350/StatefulPartitionedCall!dense_350/StatefulPartitionedCall2H
"dropout_65/StatefulPartitionedCall"dropout_65/StatefulPartitionedCall:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?"
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510410

inputs,
(dense_348_matmul_readvariableop_resource-
)dense_348_biasadd_readvariableop_resource,
(dense_349_matmul_readvariableop_resource-
)dense_349_biasadd_readvariableop_resource,
(dense_350_matmul_readvariableop_resource-
)dense_350_biasadd_readvariableop_resource
identity?? dense_348/BiasAdd/ReadVariableOp?dense_348/MatMul/ReadVariableOp? dense_349/BiasAdd/ReadVariableOp?dense_349/MatMul/ReadVariableOp? dense_350/BiasAdd/ReadVariableOp?dense_350/MatMul/ReadVariableOpw
flatten_107/ConstConst*
_output_shapes
:*
dtype0*
valueB"?????  2
flatten_107/Const?
flatten_107/ReshapeReshapeinputsflatten_107/Const:output:0*
T0*(
_output_shapes
:??????????2
flatten_107/Reshape?
dense_348/MatMul/ReadVariableOpReadVariableOp(dense_348_matmul_readvariableop_resource*
_output_shapes
:	?@*
dtype02!
dense_348/MatMul/ReadVariableOp?
dense_348/MatMulMatMulflatten_107/Reshape:output:0'dense_348/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
dense_348/MatMul?
 dense_348/BiasAdd/ReadVariableOpReadVariableOp)dense_348_biasadd_readvariableop_resource*
_output_shapes
:@*
dtype02"
 dense_348/BiasAdd/ReadVariableOp?
dense_348/BiasAddBiasAdddense_348/MatMul:product:0(dense_348/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
dense_348/BiasAddv
dense_348/ReluReludense_348/BiasAdd:output:0*
T0*'
_output_shapes
:?????????@2
dense_348/Relu?
dropout_65/IdentityIdentitydense_348/Relu:activations:0*
T0*'
_output_shapes
:?????????@2
dropout_65/Identity?
dense_349/MatMul/ReadVariableOpReadVariableOp(dense_349_matmul_readvariableop_resource*
_output_shapes

:@*
dtype02!
dense_349/MatMul/ReadVariableOp?
dense_349/MatMulMatMuldropout_65/Identity:output:0'dense_349/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_349/MatMul?
 dense_349/BiasAdd/ReadVariableOpReadVariableOp)dense_349_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02"
 dense_349/BiasAdd/ReadVariableOp?
dense_349/BiasAddBiasAdddense_349/MatMul:product:0(dense_349/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_349/BiasAddv
dense_349/ReluReludense_349/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2
dense_349/Relu?
dense_350/MatMul/ReadVariableOpReadVariableOp(dense_350_matmul_readvariableop_resource*
_output_shapes

:*
dtype02!
dense_350/MatMul/ReadVariableOp?
dense_350/MatMulMatMuldense_349/Relu:activations:0'dense_350/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_350/MatMul?
 dense_350/BiasAdd/ReadVariableOpReadVariableOp)dense_350_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02"
 dense_350/BiasAdd/ReadVariableOp?
dense_350/BiasAddBiasAdddense_350/MatMul:product:0(dense_350/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
dense_350/BiasAdd
dense_350/SoftmaxSoftmaxdense_350/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2
dense_350/Softmax?
IdentityIdentitydense_350/Softmax:softmax:0!^dense_348/BiasAdd/ReadVariableOp ^dense_348/MatMul/ReadVariableOp!^dense_349/BiasAdd/ReadVariableOp ^dense_349/MatMul/ReadVariableOp!^dense_350/BiasAdd/ReadVariableOp ^dense_350/MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2D
 dense_348/BiasAdd/ReadVariableOp dense_348/BiasAdd/ReadVariableOp2B
dense_348/MatMul/ReadVariableOpdense_348/MatMul/ReadVariableOp2D
 dense_349/BiasAdd/ReadVariableOp dense_349/BiasAdd/ReadVariableOp2B
dense_349/MatMul/ReadVariableOpdense_349/MatMul/ReadVariableOp2D
 dense_350/BiasAdd/ReadVariableOp dense_350/BiasAdd/ReadVariableOp2B
dense_350/MatMul/ReadVariableOpdense_350/MatMul/ReadVariableOp:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?
d
H__inference_flatten_107_layer_call_and_return_conditional_losses_1510102

inputs
identity_
ConstConst*
_output_shapes
:*
dtype0*
valueB"?????  2
Consth
ReshapeReshapeinputsConst:output:0*
T0*(
_output_shapes
:??????????2	
Reshapee
IdentityIdentityReshape:output:0*
T0*(
_output_shapes
:??????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????G:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?
?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510267

inputs
dense_348_1510250
dense_348_1510252
dense_349_1510256
dense_349_1510258
dense_350_1510261
dense_350_1510263
identity??!dense_348/StatefulPartitionedCall?!dense_349/StatefulPartitionedCall?!dense_350/StatefulPartitionedCall?"dropout_65/StatefulPartitionedCall?
flatten_107/PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *(
_output_shapes
:??????????* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *Q
fLRJ
H__inference_flatten_107_layer_call_and_return_conditional_losses_15101022
flatten_107/PartitionedCall?
!dense_348/StatefulPartitionedCallStatefulPartitionedCall$flatten_107/PartitionedCall:output:0dense_348_1510250dense_348_1510252*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_348_layer_call_and_return_conditional_losses_15101212#
!dense_348/StatefulPartitionedCall?
"dropout_65/StatefulPartitionedCallStatefulPartitionedCall*dense_348/StatefulPartitionedCall:output:0*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????@* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *P
fKRI
G__inference_dropout_65_layer_call_and_return_conditional_losses_15101492$
"dropout_65/StatefulPartitionedCall?
!dense_349/StatefulPartitionedCallStatefulPartitionedCall+dropout_65/StatefulPartitionedCall:output:0dense_349_1510256dense_349_1510258*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_349_layer_call_and_return_conditional_losses_15101782#
!dense_349/StatefulPartitionedCall?
!dense_350/StatefulPartitionedCallStatefulPartitionedCall*dense_349/StatefulPartitionedCall:output:0dense_350_1510261dense_350_1510263*
Tin
2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*$
_read_only_resource_inputs
*-
config_proto

CPU

GPU 2J 8? *O
fJRH
F__inference_dense_350_layer_call_and_return_conditional_losses_15102052#
!dense_350/StatefulPartitionedCall?
IdentityIdentity*dense_350/StatefulPartitionedCall:output:0"^dense_348/StatefulPartitionedCall"^dense_349/StatefulPartitionedCall"^dense_350/StatefulPartitionedCall#^dropout_65/StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2F
!dense_348/StatefulPartitionedCall!dense_348/StatefulPartitionedCall2F
!dense_349/StatefulPartitionedCall!dense_349/StatefulPartitionedCall2F
!dense_350/StatefulPartitionedCall!dense_350/StatefulPartitionedCall2H
"dropout_65/StatefulPartitionedCall"dropout_65/StatefulPartitionedCall:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?	
?
F__inference_dense_350_layer_call_and_return_conditional_losses_1510205

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2	
BiasAdda
SoftmaxSoftmaxBiasAdd:output:0*
T0*'
_output_shapes
:?????????2	
Softmax?
IdentityIdentitySoftmax:softmax:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:O K
'
_output_shapes
:?????????
 
_user_specified_nameinputs
?
e
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510154

inputs

identity_1Z
IdentityIdentityinputs*
T0*'
_output_shapes
:?????????@2

Identityi

Identity_1IdentityIdentity:output:0*
T0*'
_output_shapes
:?????????@2

Identity_1"!

identity_1Identity_1:output:0*&
_input_shapes
:?????????@:O K
'
_output_shapes
:?????????@
 
_user_specified_nameinputs
?
?
0__inference_sequential_109_layer_call_fn_1510320
flatten_107_input
unknown
	unknown_0
	unknown_1
	unknown_2
	unknown_3
	unknown_4
identity??StatefulPartitionedCall?
StatefulPartitionedCallStatefulPartitionedCallflatten_107_inputunknown	unknown_0	unknown_1	unknown_2	unknown_3	unknown_4*
Tin
	2*
Tout
2*
_collective_manager_ids
 *'
_output_shapes
:?????????*(
_read_only_resource_inputs

*-
config_proto

CPU

GPU 2J 8? *T
fORM
K__inference_sequential_109_layer_call_and_return_conditional_losses_15103052
StatefulPartitionedCall?
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::22
StatefulPartitionedCallStatefulPartitionedCall:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?
I
-__inference_flatten_107_layer_call_fn_1510455

inputs
identity?
PartitionedCallPartitionedCallinputs*
Tin
2*
Tout
2*
_collective_manager_ids
 *(
_output_shapes
:??????????* 
_read_only_resource_inputs
 *-
config_proto

CPU

GPU 2J 8? *Q
fLRJ
H__inference_flatten_107_layer_call_and_return_conditional_losses_15101022
PartitionedCallm
IdentityIdentityPartitionedCall:output:0*
T0*(
_output_shapes
:??????????2

Identity"
identityIdentity:output:0*.
_input_shapes
:?????????G:W S
/
_output_shapes
:?????????G
 
_user_specified_nameinputs
?,
?
"__inference__wrapped_model_1510092
flatten_107_input;
7sequential_109_dense_348_matmul_readvariableop_resource<
8sequential_109_dense_348_biasadd_readvariableop_resource;
7sequential_109_dense_349_matmul_readvariableop_resource<
8sequential_109_dense_349_biasadd_readvariableop_resource;
7sequential_109_dense_350_matmul_readvariableop_resource<
8sequential_109_dense_350_biasadd_readvariableop_resource
identity??/sequential_109/dense_348/BiasAdd/ReadVariableOp?.sequential_109/dense_348/MatMul/ReadVariableOp?/sequential_109/dense_349/BiasAdd/ReadVariableOp?.sequential_109/dense_349/MatMul/ReadVariableOp?/sequential_109/dense_350/BiasAdd/ReadVariableOp?.sequential_109/dense_350/MatMul/ReadVariableOp?
 sequential_109/flatten_107/ConstConst*
_output_shapes
:*
dtype0*
valueB"?????  2"
 sequential_109/flatten_107/Const?
"sequential_109/flatten_107/ReshapeReshapeflatten_107_input)sequential_109/flatten_107/Const:output:0*
T0*(
_output_shapes
:??????????2$
"sequential_109/flatten_107/Reshape?
.sequential_109/dense_348/MatMul/ReadVariableOpReadVariableOp7sequential_109_dense_348_matmul_readvariableop_resource*
_output_shapes
:	?@*
dtype020
.sequential_109/dense_348/MatMul/ReadVariableOp?
sequential_109/dense_348/MatMulMatMul+sequential_109/flatten_107/Reshape:output:06sequential_109/dense_348/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2!
sequential_109/dense_348/MatMul?
/sequential_109/dense_348/BiasAdd/ReadVariableOpReadVariableOp8sequential_109_dense_348_biasadd_readvariableop_resource*
_output_shapes
:@*
dtype021
/sequential_109/dense_348/BiasAdd/ReadVariableOp?
 sequential_109/dense_348/BiasAddBiasAdd)sequential_109/dense_348/MatMul:product:07sequential_109/dense_348/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2"
 sequential_109/dense_348/BiasAdd?
sequential_109/dense_348/ReluRelu)sequential_109/dense_348/BiasAdd:output:0*
T0*'
_output_shapes
:?????????@2
sequential_109/dense_348/Relu?
"sequential_109/dropout_65/IdentityIdentity+sequential_109/dense_348/Relu:activations:0*
T0*'
_output_shapes
:?????????@2$
"sequential_109/dropout_65/Identity?
.sequential_109/dense_349/MatMul/ReadVariableOpReadVariableOp7sequential_109_dense_349_matmul_readvariableop_resource*
_output_shapes

:@*
dtype020
.sequential_109/dense_349/MatMul/ReadVariableOp?
sequential_109/dense_349/MatMulMatMul+sequential_109/dropout_65/Identity:output:06sequential_109/dense_349/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2!
sequential_109/dense_349/MatMul?
/sequential_109/dense_349/BiasAdd/ReadVariableOpReadVariableOp8sequential_109_dense_349_biasadd_readvariableop_resource*
_output_shapes
:*
dtype021
/sequential_109/dense_349/BiasAdd/ReadVariableOp?
 sequential_109/dense_349/BiasAddBiasAdd)sequential_109/dense_349/MatMul:product:07sequential_109/dense_349/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2"
 sequential_109/dense_349/BiasAdd?
sequential_109/dense_349/ReluRelu)sequential_109/dense_349/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2
sequential_109/dense_349/Relu?
.sequential_109/dense_350/MatMul/ReadVariableOpReadVariableOp7sequential_109_dense_350_matmul_readvariableop_resource*
_output_shapes

:*
dtype020
.sequential_109/dense_350/MatMul/ReadVariableOp?
sequential_109/dense_350/MatMulMatMul+sequential_109/dense_349/Relu:activations:06sequential_109/dense_350/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2!
sequential_109/dense_350/MatMul?
/sequential_109/dense_350/BiasAdd/ReadVariableOpReadVariableOp8sequential_109_dense_350_biasadd_readvariableop_resource*
_output_shapes
:*
dtype021
/sequential_109/dense_350/BiasAdd/ReadVariableOp?
 sequential_109/dense_350/BiasAddBiasAdd)sequential_109/dense_350/MatMul:product:07sequential_109/dense_350/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????2"
 sequential_109/dense_350/BiasAdd?
 sequential_109/dense_350/SoftmaxSoftmax)sequential_109/dense_350/BiasAdd:output:0*
T0*'
_output_shapes
:?????????2"
 sequential_109/dense_350/Softmax?
IdentityIdentity*sequential_109/dense_350/Softmax:softmax:00^sequential_109/dense_348/BiasAdd/ReadVariableOp/^sequential_109/dense_348/MatMul/ReadVariableOp0^sequential_109/dense_349/BiasAdd/ReadVariableOp/^sequential_109/dense_349/MatMul/ReadVariableOp0^sequential_109/dense_350/BiasAdd/ReadVariableOp/^sequential_109/dense_350/MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????2

Identity"
identityIdentity:output:0*F
_input_shapes5
3:?????????G::::::2b
/sequential_109/dense_348/BiasAdd/ReadVariableOp/sequential_109/dense_348/BiasAdd/ReadVariableOp2`
.sequential_109/dense_348/MatMul/ReadVariableOp.sequential_109/dense_348/MatMul/ReadVariableOp2b
/sequential_109/dense_349/BiasAdd/ReadVariableOp/sequential_109/dense_349/BiasAdd/ReadVariableOp2`
.sequential_109/dense_349/MatMul/ReadVariableOp.sequential_109/dense_349/MatMul/ReadVariableOp2b
/sequential_109/dense_350/BiasAdd/ReadVariableOp/sequential_109/dense_350/BiasAdd/ReadVariableOp2`
.sequential_109/dense_350/MatMul/ReadVariableOp.sequential_109/dense_350/MatMul/ReadVariableOp:b ^
/
_output_shapes
:?????????G
+
_user_specified_nameflatten_107_input
?	
?
F__inference_dense_348_layer_call_and_return_conditional_losses_1510121

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity??BiasAdd/ReadVariableOp?MatMul/ReadVariableOp?
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes
:	?@*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2
MatMul?
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:@*
dtype02
BiasAdd/ReadVariableOp?
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:?????????@2	
BiasAddX
ReluReluBiasAdd:output:0*
T0*'
_output_shapes
:?????????@2
Relu?
IdentityIdentityRelu:activations:0^BiasAdd/ReadVariableOp^MatMul/ReadVariableOp*
T0*'
_output_shapes
:?????????@2

Identity"
identityIdentity:output:0*/
_input_shapes
:??????????::20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp2.
MatMul/ReadVariableOpMatMul/ReadVariableOp:P L
(
_output_shapes
:??????????
 
_user_specified_nameinputs"?L
saver_filename:0StatefulPartitionedCall_1:0StatefulPartitionedCall_28"
saved_model_main_op

NoOp*>
__saved_model_init_op%#
__saved_model_init_op

NoOp*?
serving_default?
W
flatten_107_inputB
#serving_default_flatten_107_input:0?????????G=
	dense_3500
StatefulPartitionedCall:0?????????tensorflow/serving/predict:??
?)
layer-0
layer_with_weights-0
layer-1
layer-2
layer_with_weights-1
layer-3
layer_with_weights-2
layer-4
	optimizer
regularization_losses
	variables
	trainable_variables

	keras_api

signatures
*`&call_and_return_all_conditional_losses
a__call__
b_default_save_signature"?'
_tf_keras_sequential?&{"class_name": "Sequential", "name": "sequential_109", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "must_restore_from_config": false, "config": {"name": "sequential_109", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "flatten_107_input"}}, {"class_name": "Flatten", "config": {"name": "flatten_107", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "dtype": "float32", "data_format": "channels_last"}}, {"class_name": "Dense", "config": {"name": "dense_348", "trainable": true, "dtype": "float32", "units": 64, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_65", "trainable": true, "dtype": "float32", "rate": 0.2, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_349", "trainable": true, "dtype": "float32", "units": 16, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dense", "config": {"name": "dense_350", "trainable": true, "dtype": "float32", "units": 8, "activation": "softmax", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 1, "axes": {}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 6, 71, 1]}, "is_graph_network": true, "keras_version": "2.4.0", "backend": "tensorflow", "model_config": {"class_name": "Sequential", "config": {"name": "sequential_109", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "flatten_107_input"}}, {"class_name": "Flatten", "config": {"name": "flatten_107", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "dtype": "float32", "data_format": "channels_last"}}, {"class_name": "Dense", "config": {"name": "dense_348", "trainable": true, "dtype": "float32", "units": 64, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_65", "trainable": true, "dtype": "float32", "rate": 0.2, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_349", "trainable": true, "dtype": "float32", "units": 16, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dense", "config": {"name": "dense_350", "trainable": true, "dtype": "float32", "units": 8, "activation": "softmax", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}}, "training_config": {"loss": "categorical_crossentropy", "metrics": [[{"class_name": "MeanMetricWrapper", "config": {"name": "accuracy", "dtype": "float32", "fn": "categorical_accuracy"}}]], "weighted_metrics": null, "loss_weights": null, "optimizer_config": {"class_name": "Adam", "config": {"name": "Adam", "learning_rate": 0.00010000000474974513, "decay": 0.0, "beta_1": 0.8999999761581421, "beta_2": 0.9990000128746033, "epsilon": 1e-07, "amsgrad": false}}}}
?
regularization_losses
	variables
trainable_variables
	keras_api
*c&call_and_return_all_conditional_losses
d__call__"?
_tf_keras_layer?{"class_name": "Flatten", "name": "flatten_107", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "stateful": false, "must_restore_from_config": false, "config": {"name": "flatten_107", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 6, 71, 1]}, "dtype": "float32", "data_format": "channels_last"}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 1, "axes": {}}}}
?

kernel
bias
regularization_losses
	variables
trainable_variables
	keras_api
*e&call_and_return_all_conditional_losses
f__call__"?
_tf_keras_layer?{"class_name": "Dense", "name": "dense_348", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "config": {"name": "dense_348", "trainable": true, "dtype": "float32", "units": 64, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 426}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 426]}}
?
regularization_losses
	variables
trainable_variables
	keras_api
*g&call_and_return_all_conditional_losses
h__call__"?
_tf_keras_layer?{"class_name": "Dropout", "name": "dropout_65", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "config": {"name": "dropout_65", "trainable": true, "dtype": "float32", "rate": 0.2, "noise_shape": null, "seed": null}}
?

kernel
bias
regularization_losses
	variables
trainable_variables
	keras_api
*i&call_and_return_all_conditional_losses
j__call__"?
_tf_keras_layer?{"class_name": "Dense", "name": "dense_349", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "config": {"name": "dense_349", "trainable": true, "dtype": "float32", "units": 16, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 64}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 64]}}
?

 kernel
!bias
"regularization_losses
#	variables
$trainable_variables
%	keras_api
*k&call_and_return_all_conditional_losses
l__call__"?
_tf_keras_layer?{"class_name": "Dense", "name": "dense_350", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "config": {"name": "dense_350", "trainable": true, "dtype": "float32", "units": 8, "activation": "softmax", "use_bias": true, "kernel_initializer": {"class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 16}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 16]}}
?
&iter

'beta_1

(beta_2
	)decay
*learning_ratemTmUmVmW mX!mYvZv[v\v] v^!v_"
	optimizer
 "
trackable_list_wrapper
J
0
1
2
3
 4
!5"
trackable_list_wrapper
J
0
1
2
3
 4
!5"
trackable_list_wrapper
?
regularization_losses
	variables

+layers
,non_trainable_variables
	trainable_variables
-layer_metrics
.layer_regularization_losses
/metrics
a__call__
b_default_save_signature
*`&call_and_return_all_conditional_losses
&`"call_and_return_conditional_losses"
_generic_user_object
,
mserving_default"
signature_map
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
?
regularization_losses
	variables

0layers
1non_trainable_variables
trainable_variables
2layer_metrics
3layer_regularization_losses
4metrics
d__call__
*c&call_and_return_all_conditional_losses
&c"call_and_return_conditional_losses"
_generic_user_object
#:!	?@2dense_348/kernel
:@2dense_348/bias
 "
trackable_list_wrapper
.
0
1"
trackable_list_wrapper
.
0
1"
trackable_list_wrapper
?
regularization_losses
	variables

5layers
6non_trainable_variables
trainable_variables
7layer_metrics
8layer_regularization_losses
9metrics
f__call__
*e&call_and_return_all_conditional_losses
&e"call_and_return_conditional_losses"
_generic_user_object
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
?
regularization_losses
	variables

:layers
;non_trainable_variables
trainable_variables
<layer_metrics
=layer_regularization_losses
>metrics
h__call__
*g&call_and_return_all_conditional_losses
&g"call_and_return_conditional_losses"
_generic_user_object
": @2dense_349/kernel
:2dense_349/bias
 "
trackable_list_wrapper
.
0
1"
trackable_list_wrapper
.
0
1"
trackable_list_wrapper
?
regularization_losses
	variables

?layers
@non_trainable_variables
trainable_variables
Alayer_metrics
Blayer_regularization_losses
Cmetrics
j__call__
*i&call_and_return_all_conditional_losses
&i"call_and_return_conditional_losses"
_generic_user_object
": 2dense_350/kernel
:2dense_350/bias
 "
trackable_list_wrapper
.
 0
!1"
trackable_list_wrapper
.
 0
!1"
trackable_list_wrapper
?
"regularization_losses
#	variables

Dlayers
Enon_trainable_variables
$trainable_variables
Flayer_metrics
Glayer_regularization_losses
Hmetrics
l__call__
*k&call_and_return_all_conditional_losses
&k"call_and_return_conditional_losses"
_generic_user_object
:	 (2	Adam/iter
: (2Adam/beta_1
: (2Adam/beta_2
: (2
Adam/decay
: (2Adam/learning_rate
C
0
1
2
3
4"
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
.
I0
J1"
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
?
	Ktotal
	Lcount
M	variables
N	keras_api"?
_tf_keras_metricj{"class_name": "Mean", "name": "loss", "dtype": "float32", "config": {"name": "loss", "dtype": "float32"}}
?
	Ototal
	Pcount
Q
_fn_kwargs
R	variables
S	keras_api"?
_tf_keras_metric?{"class_name": "MeanMetricWrapper", "name": "accuracy", "dtype": "float32", "config": {"name": "accuracy", "dtype": "float32", "fn": "categorical_accuracy"}}
:  (2total
:  (2count
.
K0
L1"
trackable_list_wrapper
-
M	variables"
_generic_user_object
:  (2total
:  (2count
 "
trackable_dict_wrapper
.
O0
P1"
trackable_list_wrapper
-
R	variables"
_generic_user_object
(:&	?@2Adam/dense_348/kernel/m
!:@2Adam/dense_348/bias/m
':%@2Adam/dense_349/kernel/m
!:2Adam/dense_349/bias/m
':%2Adam/dense_350/kernel/m
!:2Adam/dense_350/bias/m
(:&	?@2Adam/dense_348/kernel/v
!:@2Adam/dense_348/bias/v
':%@2Adam/dense_349/kernel/v
!:2Adam/dense_349/bias/v
':%2Adam/dense_350/kernel/v
!:2Adam/dense_350/bias/v
?2?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510410
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510382
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510243
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510222?
???
FullArgSpec1
args)?&
jself
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults?
p 

 

kwonlyargs? 
kwonlydefaults? 
annotations? *
 
?2?
0__inference_sequential_109_layer_call_fn_1510320
0__inference_sequential_109_layer_call_fn_1510427
0__inference_sequential_109_layer_call_fn_1510282
0__inference_sequential_109_layer_call_fn_1510444?
???
FullArgSpec1
args)?&
jself
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults?
p 

 

kwonlyargs? 
kwonlydefaults? 
annotations? *
 
?2?
"__inference__wrapped_model_1510092?
???
FullArgSpec
args? 
varargsjargs
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *8?5
3?0
flatten_107_input?????????G
?2?
H__inference_flatten_107_layer_call_and_return_conditional_losses_1510450?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
-__inference_flatten_107_layer_call_fn_1510455?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
F__inference_dense_348_layer_call_and_return_conditional_losses_1510466?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
+__inference_dense_348_layer_call_fn_1510475?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510492
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510487?
???
FullArgSpec)
args!?
jself
jinputs

jtraining
varargs
 
varkw
 
defaults?
p 

kwonlyargs? 
kwonlydefaults? 
annotations? *
 
?2?
,__inference_dropout_65_layer_call_fn_1510497
,__inference_dropout_65_layer_call_fn_1510502?
???
FullArgSpec)
args!?
jself
jinputs

jtraining
varargs
 
varkw
 
defaults?
p 

kwonlyargs? 
kwonlydefaults? 
annotations? *
 
?2?
F__inference_dense_349_layer_call_and_return_conditional_losses_1510513?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
+__inference_dense_349_layer_call_fn_1510522?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
F__inference_dense_350_layer_call_and_return_conditional_losses_1510533?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?2?
+__inference_dense_350_layer_call_fn_1510542?
???
FullArgSpec
args?
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 
?B?
%__inference_signature_wrapper_1510347flatten_107_input"?
???
FullArgSpec
args? 
varargs
 
varkwjkwargs
defaults
 

kwonlyargs? 
kwonlydefaults
 
annotations? *
 ?
"__inference__wrapped_model_1510092? !B??
8?5
3?0
flatten_107_input?????????G
? "5?2
0
	dense_350#? 
	dense_350??????????
F__inference_dense_348_layer_call_and_return_conditional_losses_1510466]0?-
&?#
!?
inputs??????????
? "%?"
?
0?????????@
? 
+__inference_dense_348_layer_call_fn_1510475P0?-
&?#
!?
inputs??????????
? "??????????@?
F__inference_dense_349_layer_call_and_return_conditional_losses_1510513\/?,
%?"
 ?
inputs?????????@
? "%?"
?
0?????????
? ~
+__inference_dense_349_layer_call_fn_1510522O/?,
%?"
 ?
inputs?????????@
? "???????????
F__inference_dense_350_layer_call_and_return_conditional_losses_1510533\ !/?,
%?"
 ?
inputs?????????
? "%?"
?
0?????????
? ~
+__inference_dense_350_layer_call_fn_1510542O !/?,
%?"
 ?
inputs?????????
? "???????????
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510487\3?0
)?&
 ?
inputs?????????@
p
? "%?"
?
0?????????@
? ?
G__inference_dropout_65_layer_call_and_return_conditional_losses_1510492\3?0
)?&
 ?
inputs?????????@
p 
? "%?"
?
0?????????@
? 
,__inference_dropout_65_layer_call_fn_1510497O3?0
)?&
 ?
inputs?????????@
p
? "??????????@
,__inference_dropout_65_layer_call_fn_1510502O3?0
)?&
 ?
inputs?????????@
p 
? "??????????@?
H__inference_flatten_107_layer_call_and_return_conditional_losses_1510450a7?4
-?*
(?%
inputs?????????G
? "&?#
?
0??????????
? ?
-__inference_flatten_107_layer_call_fn_1510455T7?4
-?*
(?%
inputs?????????G
? "????????????
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510222{ !J?G
@?=
3?0
flatten_107_input?????????G
p

 
? "%?"
?
0?????????
? ?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510243{ !J?G
@?=
3?0
flatten_107_input?????????G
p 

 
? "%?"
?
0?????????
? ?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510382p !??<
5?2
(?%
inputs?????????G
p

 
? "%?"
?
0?????????
? ?
K__inference_sequential_109_layer_call_and_return_conditional_losses_1510410p !??<
5?2
(?%
inputs?????????G
p 

 
? "%?"
?
0?????????
? ?
0__inference_sequential_109_layer_call_fn_1510282n !J?G
@?=
3?0
flatten_107_input?????????G
p

 
? "???????????
0__inference_sequential_109_layer_call_fn_1510320n !J?G
@?=
3?0
flatten_107_input?????????G
p 

 
? "???????????
0__inference_sequential_109_layer_call_fn_1510427c !??<
5?2
(?%
inputs?????????G
p

 
? "???????????
0__inference_sequential_109_layer_call_fn_1510444c !??<
5?2
(?%
inputs?????????G
p 

 
? "???????????
%__inference_signature_wrapper_1510347? !W?T
? 
M?J
H
flatten_107_input3?0
flatten_107_input?????????G"5?2
0
	dense_350#? 
	dense_350?????????