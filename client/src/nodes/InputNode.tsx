import { UseFormRegister } from 'react-hook-form';
import {  Handle, Position, type NodeProps } from 'reactflow';

export interface InputNodeProps {
    title: string
    description: string
    placeholder: string
    hasTextArea: boolean
    register: UseFormRegister<any>
}


export function InputNode({ data: {register, ...data} }: NodeProps<InputNodeProps>) {
    return (
        <div style={{ padding: 5, borderWidth: 4, display: 'flex', flexDirection: 'column', border: '2px solid #000000', borderRadius: 10, width: 250, height: 300, fontSize: "1.2rem" }}>
            <h2 style={{margin: "0"}}>{data.title}</h2>
            <p>{data.description}</p>
            {data.hasTextArea && <textarea
                // placeholder={data.placeholder}
                value={data.placeholder}
                {...register(data.title)}
                style={{ width: '100%', height: '50%', marginTop: 'auto',  resize: 'none' }}></textarea>}
            <Handle type='target' id='l' position={Position.Left}  />
            <Handle type='target' id='b' position={Position.Bottom} />
            <Handle type='source' id='b' position={Position.Bottom} />
            <Handle type='source' id='r' position={Position.Right} />
        </div>
    );
}

