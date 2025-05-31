

lr=(1e-03 1e-04 5e-05)
batch_size=(64 128 256)
n_layers=(1 2 4 8)
n_heads=(1 2)

for i in ${!lr[@]}; do
    for j in ${!batch_size[@]}; do
        for k in ${!n_layers[@]}; do
            for l in ${!n_heads[@]}; do
                CUDA_VISIBLE_DEVICES=0 python run_rec.py\
                    --lr ${lr[$i]}\
                    --batch_size ${batch_size[$j]}\
                    --n_layers ${n_layers[$k]}\
                    --n_heads ${n_heads[$l]}\
                    --wandb
            done
        done
    done
done


